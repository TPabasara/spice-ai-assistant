"use client";

import React, { useState, useEffect } from "react";
import { apiClient } from "@/lib/api";
import {
  Shield,
  Cpu,
  Clock,
  BarChart3,
  UploadCloud,
  RefreshCw,
} from "lucide-react";

interface SummaryData {
  total_conversations: number;
  total_tokens_consumed: number;
  average_latency_ms: number;
  average_similarity_score: number;
}

interface LogEntry {
  id: number;
  session_id: number;
  content: string;
  prompt_used: string;
  tokens_used: number;
  latency_ms: number;
  similarity_score: number;
  timestamp: string;
}

export default function AdminDashboard() {
  const [metrics, setMetrics] = useState<SummaryData | null>(null);
  const [logs, setLogs] = useState<LogEntry[]>([]);
  const [loading, setLoading] = useState(true);
  const [uploadStatus, setUploadStatus] = useState("");

  const fetchDashboardData = async () => {
    setLoading(true);
    try {
      // In a complete integration, attach token headers from storage here
      const response = await apiClient.get("/analytics/dashboard");
      setMetrics(response.data.summary);
      setLogs(response.data.recent_logs);
    } catch (err) {
      console.error("Failed to collect systems telemetries", err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    if (!e.target.files || e.target.files.length === 0) return;
    const file = e.target.files[0];
    const formData = new FormData();
    formData.append("file", file);

    setUploadStatus("Uploading knowledge file...");
    try {
      await apiClient.post("/documents/upload", formData, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      setUploadStatus("Success! File queued for embedding pipeline.");
      fetchDashboardData();
    } catch (err) {
      setUploadStatus("Upload failed. Ensure document format is PDF.");
    }
  };

  return (
    <div className="container mx-auto p-6 max-w-7xl">
      {/* Header section */}
      <div className="flex justify-between items-center border-b pb-4 mb-6">
        <div className="flex items-center gap-3">
          <Shield className="h-8 w-8 text-orange-600" />
          <h1 className="text-3xl font-bold tracking-tight">
            System Control & Telemetry
          </h1>
        </div>
        <button
          onClick={fetchDashboardData}
          className="flex items-center gap-2 px-4 py-2 border rounded-md text-sm font-medium hover:bg-slate-50 transition"
        >
          <RefreshCw className={`h-4 w-4 ${loading ? "animate-spin" : ""}`} />
          Refresh
        </button>
      </div>

      {/* Analytics Summary Cards */}
      {metrics && (
        <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-8">
          <div className="p-5 bg-white border rounded-xl shadow-sm">
            <div className="text-slate-500 text-sm font-medium">
              Conversations
            </div>
            <div className="text-2xl font-bold mt-2 text-slate-900">
              {metrics.total_conversations}
            </div>
          </div>
          <div className="p-5 bg-white border rounded-xl shadow-sm">
            <div className="flex justify-between items-center">
              <span className="text-slate-500 text-sm font-medium">
                Total Token Volume
              </span>
              <Cpu className="h-4 w-4 text-orange-500" />
            </div>
            <div className="text-2xl font-bold mt-2 text-slate-900">
              {metrics.total_tokens_consumed.toLocaleString()}
            </div>
          </div>
          <div className="p-5 bg-white border rounded-xl shadow-sm">
            <div className="flex justify-between items-center">
              <span className="text-slate-500 text-sm font-medium">
                Avg Agent Latency
              </span>
              <Clock className="h-4 w-4 text-amber-500" />
            </div>
            <div className="text-2xl font-bold mt-2 text-slate-900">
              {metrics.average_latency_ms} ms
            </div>
          </div>
          <div className="p-5 bg-white border rounded-xl shadow-sm">
            <div className="flex justify-between items-center">
              <span className="text-slate-500 text-sm font-medium">
                RAG Context Alignment
              </span>
              <BarChart3 className="h-4 w-4 text-emerald-500" />
            </div>
            <div className="text-2xl font-bold mt-2 text-slate-900">
              {metrics.average_similarity_score}
            </div>
          </div>
        </div>
      )}

      {/* Execution Operations Panel */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
        {/* Management Controls */}
        <div className="p-6 bg-white border rounded-xl shadow-sm h-fit">
          <h2 className="text-lg font-bold mb-4 flex items-center gap-2">
            <UploadCloud className="h-5 w-5 text-slate-600" />
            Knowledge Base Ingestion
          </h2>
          <div className="border-2 border-dashed border-slate-200 rounded-lg p-6 text-center hover:border-orange-400 transition cursor-pointer relative">
            <input
              type="file"
              accept=".pdf"
              onChange={handleFileUpload}
              className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
            />
            <p className="text-sm font-semibold text-slate-700">
              Drop corporate PDF assets here
            </p>
            <p className="text-xs text-slate-400 mt-1">
              Accepts Product Manuals, Policies, Guides
            </p>
          </div>
          {uploadStatus && (
            <p className="mt-4 text-xs font-medium text-orange-600 bg-orange-50 p-2 rounded border border-orange-100">
              {uploadStatus}
            </p>
          )}
        </div>

        {/* Live Trace Audit Log Table */}
        <div className="lg:col-span-2 p-6 bg-white border rounded-xl shadow-sm">
          <h2 className="text-lg font-bold mb-4">LLM Live Performance Logs</h2>
          <div className="overflow-x-auto">
            <table className="w-full text-left border-collapse text-sm">
              <thead>
                <tr className="border-b bg-slate-50 text-slate-600 font-medium">
                  <th className="p-3">Session ID</th>
                  <th className="p-3">Generated Output Sample</th>
                  <th className="p-3">Latency</th>
                  <th className="p-3">Token Cost</th>
                  <th className="p-3">Similarity</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log) => (
                  <tr
                    key={log.id}
                    className="border-b hover:bg-slate-50 transition"
                  >
                    <td className="p-3 font-mono text-xs">{log.session_id}</td>
                    <td className="p-3 max-w-xs truncate font-normal text-slate-700">
                      {log.content}
                    </td>
                    <td className="p-3 font-medium">
                      {log.latency_ms ?? 0} ms
                    </td>
                    <td className="p-3 font-mono text-xs">
                      {log.tokens_used ?? 0}
                    </td>
                    <td className="p-3 text-emerald-600 font-medium">
                      {log.similarity_score ?? "0.000"}
                    </td>
                  </tr>
                ))}
                {logs.length === 0 && (
                  <tr>
                    <td colSpan={5} className="p-4 text-center text-slate-400">
                      No telemetry execution records present.
                    </td>
                  </tr>
                )}
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  );
}
