const API_BASE_URL = (import.meta.env.VITE_API_BASE_URL || "http://localhost:8000").replace(/\/$/, "");
const API_PREFIX = `${API_BASE_URL}/api/v1`;
const TOKEN_KEY = "learnmate_access_token";

export function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function parseResponse(response) {
  if (response.status === 204) return null;
  const contentType = response.headers.get("content-type") || "";
  const body = contentType.includes("application/json") ? await response.json() : await response.text();
  if (!response.ok) {
    if (response.status === 401) {
      clearToken();
      window.dispatchEvent(new Event("learnmate:unauthorized"));
    }
    const detail = typeof body === "object" ? body.detail : body;
    throw new Error(detail || `Request failed with status ${response.status}`);
  }
  return body;
}

async function request(path, options = {}) {
  const headers = new Headers(options.headers || {});
  const token = getToken();
  if (token) headers.set("Authorization", `Bearer ${token}`);
  if (!(options.body instanceof FormData) && !headers.has("Content-Type")) {
    headers.set("Content-Type", "application/json");
  }
  const response = await fetch(`${API_PREFIX}${path}`, { ...options, headers });
  return parseResponse(response);
}

export const api = {
  async login(username, password) {
    const body = new URLSearchParams({ username, password });
    const response = await fetch(`${API_PREFIX}/auth/login`, {
      method: "POST",
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
      body,
    });
    const data = await parseResponse(response);
    setToken(data.access_token);
    return data;
  },
  register: (payload) => request("/users/", { method: "POST", body: JSON.stringify(payload) }),
  me: () => request("/users/me"),
  subjects: () => request("/subjects/"),
  createSubject: (payload) => request("/subjects/", { method: "POST", body: JSON.stringify(payload) }),
  updateSubject: (id, payload) => request(`/subjects/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteSubject: (id) => request(`/subjects/${id}`, { method: "DELETE" }),
  topics: (subjectId) => request(`/topics/?subject_id=${subjectId}`),
  topic: (id) => request(`/topics/${id}`),
  createTopic: (payload) => request("/topics/", { method: "POST", body: JSON.stringify(payload) }),
  updateTopic: (id, payload) => request(`/topics/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTopic: (id) => request(`/topics/${id}`, { method: "DELETE" }),
  tasks: (params = "") => request(`/tasks/${params ? `?${params}` : ""}`),
  createTask: (payload) => request("/tasks/", { method: "POST", body: JSON.stringify(payload) }),
  updateTask: (id, payload) => request(`/tasks/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTask: (id) => request(`/tasks/${id}`, { method: "DELETE" }),
  timetable: () => request("/timetable/"),
  createTimetable: (payload) => request("/timetable/", { method: "POST", body: JSON.stringify(payload) }),
  updateTimetable: (id, payload) => request(`/timetable/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteTimetable: (id) => request(`/timetable/${id}`, { method: "DELETE" }),
  attendanceSummary: () => request("/attendance/summary"),
  attendanceLogs: () => request("/attendance/logs"),
  subjectAttendance: (id) => request(`/attendance/subject/${id}`),
  createAttendance: (payload) => request("/attendance/", { method: "POST", body: JSON.stringify(payload) }),
  updateAttendance: (id, payload) => request(`/attendance/${id}`, { method: "PUT", body: JSON.stringify(payload) }),
  deleteAttendance: (id) => request(`/attendance/${id}`, { method: "DELETE" }),
  materials: () => request("/materials/"),
  material: (id) => request(`/materials/${id}`),
  uploadMaterial: (file, title) => {
    const form = new FormData();
    form.append("file", file);
    form.append("title", title);
    return request("/materials/upload", { method: "POST", body: form });
  },
  askMaterial: (id, question) => request(`/materials/${id}/ask`, { method: "POST", body: JSON.stringify({ question }) }),
  generateMaterial: (id, artifact_type, max_items = 5) =>
    request(`/materials/${id}/generate`, { method: "POST", body: JSON.stringify({ artifact_type, max_items }) }),
  quizQuestions: (topicId) => request(`/quizzes/questions${topicId ? `?topic_id=${topicId}` : ""}`),
  createQuizQuestion: (payload) => request("/quizzes/questions", { method: "POST", body: JSON.stringify(payload) }),
  quizAttempts: () => request("/quizzes/attempts"),
  submitQuiz: (payload) => request("/quizzes/attempts", { method: "POST", body: JSON.stringify(payload) }),
  weakTopics: () => request("/quizzes/weak-topics"),
  recommendations: () => request("/recommendations/"),
  studyPlan: () => request("/study-plans/"),
  predict: (payload) => request("/predict/", { method: "POST", body: JSON.stringify(payload) }),
};

export { API_BASE_URL };
