import os
import json
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
from pydantic import BaseModel, PrivateAttr
from langchain.tools import BaseTool


class DataAnalysisToolInput(BaseModel):
    input_str: str

class DataAnalysisTool(BaseTool):
    args_schema = DataAnalysisToolInput
    name: str = "data_analysis_tool"
    description: str = """
    Analyze air quality data from NDJSON files. This tool can:
    - Load and parse NDJSON files from data folder
    - Handle different column naming conventions (co2, CO2, CO2 (PPM), etc.)
    - Perform statistical analysis, grouping, filtering
    - Generate charts and tables
    - Handle time-based analysis (hourly, daily, weekly patterns)
    
    Input should be a JSON string with analysis parameters:
    {
        "operation": "analyze|load|chart",
        "rooms": ["room_a", "room_b", "room_c"] or "all",
        "metrics": ["temperature", "co2", "humidity"],
        "group_by": "hour|day|week|room",
        "filter": {"start_date": "YYYY-MM-DD", "end_date": "YYYY-MM-DD"},
        "chart_type": "line|bar|scatter|heatmap"
    }
    """
    _data_folder: str = PrivateAttr(default="data")
    _column_mappings: dict = PrivateAttr(default_factory=lambda: {
        'timestamp': ['timestamp', 'time', 'datetime', 'date_time', 'ts'],
        'co2': ['co2', 'CO2', 'CO2 (ppm)', 'CO2 (PPM)'],
        'humidity': ['rh', 'Relative Humidity (%)', 'RH'],
        'temperature': ['temp', 'Temp', 'Temperature (\u00b0C)'],
    })

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # PrivateAttrs are set automatically

    def _run(self, input_str: str = '', input: str = '') -> str:
        # Accept both input_str and input for compatibility
        if not input_str and input:
            input_str = input
        if not input_str:
            return "Error: No input provided to data_analysis_tool"
        try:
            params = json.loads(input_str)
            operation = params.get('operation', 'analyze')
            if operation == 'load':
                return self._load_data_info()
            elif operation == 'analyze':
                result = self._analyze_data(params)
                return result if result is not None else f"Error: unable to analyze data" 
            elif operation == 'chart':
                return self._create_chart(params)
            else:
                return "Unknown operation. Use 'load', 'analyze', or 'chart'."
        except Exception as e:
            return f"Error: {str(e)}"

    def _load_data_info(self) -> str:
        """Load and return information about available data files"""
        try:
            files_info = []
            for filename in os.listdir(self._data_folder):
                if filename.endswith('.ndjson'):
                    filepath = os.path.join(self._data_folder, filename)
                    with open(filepath, 'r') as f:
                        first_line = f.readline()
                        if first_line:
                            sample_data = json.loads(first_line)
                            files_info.append({
                                'filename': filename,
                                'room': filename.replace('.ndjson', ''),
                                'columns': list(sample_data.keys()),
                                'sample_data': sample_data
                            })
            return json.dumps(files_info, indent=2)
        except Exception as e:
            return f"Error loading data info: {str(e)}"

    def _normalize_column_name(self, columns: List[str], target_metric: str) -> Optional[str]:
        """Find the actual column name for a target metric"""
        possible_names = self._column_mappings.get(target_metric, [])
        for col in columns:
            if col.lower() in [name.lower() for name in possible_names]:
                return col
        return None

    def _load_room_data(self, room_name: str) -> pd.DataFrame:
        """Load data for a specific room"""
        filename = f"{room_name}.ndjson"
        filepath = os.path.join(self._data_folder, filename)
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"Data file for {room_name} not found")
        data = []
        with open(filepath, 'r') as f:
            for line in f:
                if line.strip():
                    data.append(json.loads(line))
        df = pd.DataFrame(data)
        # Normalize column names
        column_map = {}
        for target_metric in ['co2', 'temperature', 'humidity', 'timestamp']:
            actual_col = self._normalize_column_name(df.columns.tolist(), target_metric)
            if actual_col:
                column_map[actual_col] = target_metric
        df = df.rename(columns=column_map)
        # Parse timestamp
        if 'timestamp' in df.columns:
            df['timestamp'] = pd.to_datetime(df['timestamp'])
            df['hour'] = df['timestamp'].dt.hour
            df['day_of_week'] = df['timestamp'].dt.day_name()
            df['date'] = df['timestamp'].dt.date
        df['room'] = room_name
        return df

    def _analyze_data(self, params: Dict) -> Optional[str]:
        """Perform data analysis based on parameters"""
        try:
            rooms = params.get('rooms', 'all')
            if rooms == 'all':
                rooms = ['room_a', 'room_b', 'room_c', 'room_d']
            
            # Load data for specified rooms
            all_data = []
            for room in rooms:
                try:
                    room_data = self._load_room_data(room)
                    all_data.append(room_data)
                except FileNotFoundError:
                    continue
            
            if not all_data:
                return "No data files found"
            
            combined_df = pd.concat(all_data, ignore_index=True)
            
            # Apply filters if specified
            filter_params = params.get('filter', {})
            if 'start_date' in filter_params:
                start_date = pd.to_datetime(filter_params['start_date'])
                # combined_df = combined_df[combined_df['timestamp'] >= start_date]
                combined_df = combined_df.loc[combined_df['timestamp'] >= start_date]
            if 'end_date' in filter_params:
                end_date = pd.to_datetime(filter_params['end_date'])
                # combined_df = combined_df[combined_df['timestamp'] <= end_date]
                combined_df = combined_df.loc[combined_df['timestamp'] <= end_date]
            
            # Perform grouping and aggregation
            group_by = params.get('group_by', 'room')
            metrics = params.get('metrics', ['temperature', 'co2', 'humidity'])
            
            available_metrics = [m for m in metrics if m in combined_df.columns]
            
            if group_by == 'hour':
                result = combined_df.groupby('hour')[available_metrics].mean().round(2)
            elif group_by == 'day':
                result = combined_df.groupby('day_of_week')[available_metrics].mean().round(2)
            elif group_by == 'room':
                result = combined_df.groupby('room')[available_metrics].agg(['mean', 'min', 'max', 'std']).round(2)
            elif group_by == 'date':
                result = combined_df.groupby('date')[available_metrics].mean().round(2)
            else:
                result = combined_df[['room'] + available_metrics].describe()
            
            return result.to_json(orient='index', indent=2)
            
        except Exception as e:
            return f"Analysis error: {str(e)}"
    
    def _create_chart(self, params: Dict) -> str:
        """Create chart data for visualization"""
        try:
            # This method returns chart configuration that can be used by the frontend
            analysis_result = self._analyze_data(params)
            if analysis_result is None:
                return "Error: unable to analyze data"

            chart_type = params.get('chart_type', 'line')
            
            chart_config = {
                'type': chart_type,
                'data': json.loads(analysis_result),
                'title': f"Air Quality Analysis - {params.get('group_by', 'room').title()}",
                'x_axis': params.get('group_by', 'room'),
                'y_axis': params.get('metrics', ['temperature'])[0]
            }
            
            return json.dumps(chart_config)
            
        except Exception as e:
            return f"Chart creation error: {str(e)}"
