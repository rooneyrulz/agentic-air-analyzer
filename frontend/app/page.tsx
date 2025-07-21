"use client";

import React, { useState } from "react";
import {
  Card,
  CardHeader,
  CardTitle,
  CardDescription,
  CardContent,
  CardFooter,
} from "@/components/ui/card";
import { Input } from "@/components/ui/input";
import { Button } from "@/components/ui/button";
import { Table, TableHeader, TableRow, TableHead, TableBody, TableCell } from "@/components/ui/table";
import { Alert, AlertTitle, AlertDescription } from "@/components/ui/alert";
import { Loader2, Search, BarChart3, TrendingUp, Thermometer, Wind, Sparkles } from "lucide-react";

const exampleQueries = [
  "How does the temperature in Room A change by hour of the day?",
  "How does CO2 vary by day of the week?",
  "Which room had the highest temperature reading last week?",
  "Which room had the biggest variation in CO2 levels?",
  "List the rooms in order of hottest to coolest using average temperature",
  "What is the average temperature of each room in mornings and evenings?",
];

export default function AirQualityAnalyzer() {
  const [query, setQuery] = useState("");
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!query.trim()) return;

    setLoading(true);
    setError(null);

    try {
      const res = await fetch("http://localhost:8000/query", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query.trim() }),
      });
      if (!res.ok) throw new Error(`HTTP error! status: ${res.status}`);
      const data = await res.json();
      setResponse(data);
    } catch (err: any) {
      setError(err.message || "An error occurred while processing your query");
    } finally {
      setLoading(false);
    }
  };

  const renderTable = (tableData: any[]) => {
    if (!tableData || tableData.length === 0) return null;
    const headers = Object.keys(tableData[0]);
    return (
      <Table>
        <TableHeader>
          <TableRow>
            {headers.map((header) => (
              <TableHead key={header}>{header}</TableHead>
            ))}
          </TableRow>
        </TableHeader>
        <TableBody>
          {tableData.map((row, rowIndex) => (
            <TableRow key={rowIndex}>
              {headers.map((header) => (
                <TableCell key={header}>{row[header]}</TableCell>
              ))}
            </TableRow>
          ))}
        </TableBody>
      </Table>
    );
  };

  const formatResponse = (text: string) => {
    // Simple formatting, can be improved for markdown
    return text.split("\n").map((line, i) => <div key={i}>{line}</div>);
  };

  return (
    <div className="bg-gradient-to-br from-blue-50 via-white to-indigo-50">
      {/* Header */}
      <Card className="mb-6 w-full">
        <CardHeader className="container mx-auto flex flex-row items-center gap-4">
          <span className="rounded-full bg-primary/10 p-2">
            <Sparkles className="h-10 w-10 text-primary" />
          </span>
          <div>
            <CardTitle className="text-3xl">Agentic Air Analyzer</CardTitle>
            <CardDescription>
              Gain insights into rooms air quality with a single click.
            </CardDescription>
          </div>
        </CardHeader>
      </Card>

      {/* Query Form */}
      <Card className="mx-auto mb-6 container">
        <form onSubmit={handleSubmit}>
          <CardContent className="flex items-center gap-4 py-6">
            <div className="relative flex-1">
              <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-gray-400 h-6 w-6" />
              <Input
                type="text"
                value={query}
                onChange={(e) => setQuery(e.target.value)}
                placeholder="Ask about air quality data..."
                className="pl-12 h-14"
                disabled={loading}
              />
            </div>
            <Button
              type="submit"
              disabled={loading || !query.trim()}
              className="flex items-center gap-2 h-14"
            >
              {loading ? (
                <>
                  <Loader2 className="animate-spin h-6 w-6" />
                  Analyzing...
                </>
              ) : (
                <>
                  <BarChart3 className="h-6 w-6" />
                  Analyze
                </>
              )}
            </Button>
          </CardContent>
        </form>
      </Card>

      {/* Example Queries */}
      {!response && (
        <Card className="container mx-auto mb-6">
          <CardHeader>
            <CardTitle className="flex items-center gap-2 text-xl">
              <TrendingUp className="h-5 w-5 text-blue-500" />
              Example Queries
            </CardTitle>
          </CardHeader>
          <CardContent>
            <div className="flex flex-wrap gap-3">
              {exampleQueries.map((example, idx) => (
                <Button
                  key={idx}
                  variant="outline"
                  className="justify-start flex-grow h-14 text-left"
                  onClick={() => setQuery(example)}
                >
                  {example}
                </Button>
              ))}
            </div>
          </CardContent>
        </Card>
      )}

      {/* Error Display */}
      {error && (
        <Alert variant="destructive" className="container mx-auto mb-6">
          <AlertTitle>Error Processing Query</AlertTitle>
          <AlertDescription>{error}</AlertDescription>
        </Alert>
      )}

      {/* Results Display */}
      {response && (
        <div className="container mx-auto space-y-6">
          {/* Answer Text */}
          {response.answer && (
            <Card>
              <CardHeader className="flex items-center gap-2">
                <Thermometer className="h-5 w-5 text-green-500" />
                <CardTitle>Analysis Results</CardTitle>
              </CardHeader>
              <CardContent>
                <div className="prose prose-blue max-w-none">
                  {formatResponse(response.answer)}
                </div>
              </CardContent>
            </Card>
          )}

          {/* Table Data */}
          {response.table_data && response.table_data.length > 0 && (
            <Card>
              <CardHeader className="flex items-center gap-2">
                <BarChart3 className="h-5 w-5 text-purple-500" />
                <CardTitle>Data Table</CardTitle>
              </CardHeader>
              <CardContent>{renderTable(response.table_data)}</CardContent>
            </Card>
          )}

          {/* Chart Placeholder */}
          {response.chart_type && (
            <Card>
              <CardHeader className="flex items-center gap-2">
                <TrendingUp className="h-5 w-5 text-indigo-500" />
                <CardTitle>
                  Visualization ({response.chart_type})
                </CardTitle>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col items-center justify-center py-8 text-gray-500">
                  <BarChart3 className="h-16 w-16 mb-4 opacity-30" />
                  <p className="text-lg font-medium">Chart visualization coming soon</p>
                  <p className="text-sm mt-2">
                    Suggested chart type: {response.chart_type}
                  </p>
                </div>
              </CardContent>
            </Card>
          )}
        </div>
      )}

      {/* Footer */}
      <div className="container mx-auto py-8">
        <p className="text-center text-gray-500 text-sm">
          Powered by AI Agent with LangChain • Supports natural language queries for air quality data analysis
        </p>
      </div>
    </div>
  );
}