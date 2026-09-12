import { Navigate, Route, Routes } from "react-router-dom";
import { AuthProvider, useAuth } from "./context/AuthContext";
import { AppShell } from "./components/Layout";
import { LoginPage, RegisterPage } from "./pages/AuthPages";
import {
  AttendancePage,
  DashboardPage,
  MaterialsPage,
  MaterialDetailPage,
  PredictionsPage,
  ProfilePage,
  QuizzesPage,
  RecommendationsPage,
  StudyPlanPage,
  SubjectsPage,
  TasksPage,
  TimetablePage,
  TopicsPage,
} from "./pages/AppPages";

function ProtectedRoutes() {
  const { user, loading } = useAuth();

  if (loading) {
    return <div className="page-loading">Loading your workspace...</div>;
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <AppShell>
      <Routes>
        <Route path="/dashboard" element={<DashboardPage />} />
        <Route path="/subjects" element={<SubjectsPage />} />
        <Route path="/subjects/:subjectId" element={<SubjectsPage />} />
        <Route path="/topics" element={<TopicsPage />} />
        <Route path="/tasks" element={<TasksPage />} />
        <Route path="/timetable" element={<TimetablePage />} />
        <Route path="/attendance" element={<AttendancePage />} />
        <Route path="/materials" element={<MaterialsPage />} />
        <Route path="/materials/:documentId" element={<MaterialDetailPage />} />
        <Route path="/quizzes" element={<QuizzesPage />} />
        <Route path="/recommendations" element={<RecommendationsPage />} />
        <Route path="/study-plan" element={<StudyPlanPage />} />
        <Route path="/predictions" element={<PredictionsPage />} />
        <Route path="/profile" element={<ProfilePage />} />
        <Route path="*" element={<Navigate to="/dashboard" replace />} />
      </Routes>
    </AppShell>
  );
}

function AppRoutes() {
  return (
    <Routes>
      <Route path="/login" element={<LoginPage />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/*" element={<ProtectedRoutes />} />
    </Routes>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppRoutes />
    </AuthProvider>
  );
}
