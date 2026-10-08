import axios from "axios";

const api = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "http://localhost:8000",
});

api.interceptors.request.use((config) => {
  const userId = localStorage.getItem("userId");
  if (userId) {
    config.headers["X-User-Id"] = userId;
  }
  return config;
});

export const getCurrentUser = async () => {
  const { data } = await api.get("/api/users/me");
  return data;
};

export const loginUser = async (payload) => {
  const { data } = await api.post("/api/users/login", payload);
  localStorage.setItem("userId", String(data.user_id));
  return data;
};

export const registerUser = async (payload) => {
  const { data } = await api.post("/api/users/register", payload);
  localStorage.setItem("userId", String(data.user_id));
  return data;
};

export const updateUser = async (payload) => {
  const { data } = await api.put("/api/users/me", payload);
  return data;
};

export const getProfile = async () => {
  const { data } = await api.get("/api/profiles/me");
  return data;
};

export const createProfile = async (payload) => {
  const { data } = await api.post("/api/profiles/me", payload);
  return data;
};

export const updateProfile = async (payload) => {
  const { data } = await api.put("/api/profiles/me", payload);
  return data;
};

export const getHealthMetrics = async () => {
  const { data } = await api.get("/api/health-metrics");
  return data;
};

export const createHealthMetric = async (payload) => {
  const { data } = await api.post("/api/health-metrics", payload);
  return data;
};

export const getConstraints = async () => {
  const { data } = await api.get("/api/constraints");
  return data;
};

export const createConstraint = async (payload) => {
  const { data } = await api.post("/api/constraints", payload);
  return data;
};

export const getDietPlans = async () => {
  const { data } = await api.get("/api/diet-plans");
  return data;
};

export const createDietPlan = async (payload) => {
  const { data } = await api.post("/api/diet-plans", payload);
  return data;
};

export const logoutUser = () => {
  localStorage.removeItem("userId");
};

export default api;
