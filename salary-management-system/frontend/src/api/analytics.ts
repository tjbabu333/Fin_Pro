import apiClient from "./client";
import type { Analytics } from "../types/analytics";

export async function getAnalytics(): Promise<Analytics> {
  const response = await apiClient.get("/analytics");

  return response.data;
}