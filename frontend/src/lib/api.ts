import axios from "axios";

// Default to localhost:8000 if the environment variable is missing
const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000/api/v1";

export const apiClient = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    "Content-Type": "application/json",
  },
});

// A quick utility function to check backend health
export const checkBackendHealth = async () => {
  try {
    const response = await apiClient.get("/system/health");
    return response.data;
  } catch (error) {
    console.error("Backend connection failed:", error);
    throw error;
  }
};
