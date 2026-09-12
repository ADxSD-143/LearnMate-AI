import { useEffect, useMemo, useState } from "react";
import { Link, useNavigate, useParams } from "react-router-dom";
import { api } from "../api";
import { useAuth } from "../context/AuthContext";
import {
  Button,
  Card,
  EmptyState,
  ErrorState,
  Field,
  LoadingState,
  Modal,
  PageHeader,
  StatCard,
  formatDate,
} from "../components/UI";

function useResource(loader, dependencies = []) {
  const [state, setState] = useState({ data: null, loading: true, error: "" });
  async function reload() {
    setState({ data: null, loading: true, error: "" });
    try {
      setState({ data: await loader(), loading: false, error: "" });
    } catch (error) {
      setState({ data: null, loading: false, error: error.message });
    }
  }
  useEffect(() => { reload(); }, dependencies);
  return { ...state, reload };
}

function PageState({ resource, children }) {
  if (resource.loading) return <LoadingState />;
  if (resource.error) return <ErrorState message={resource.error} onRetry={resource.reload} />;
  return children(resource.data);
}

function ProgressBar({ value }) {
  const safe = Math.max(0, Math.min(100, Number(value) || 0));
  return <div className="progress-track"><span style={{ width: `${safe}%` }} /></div>;
}

export function DashboardPage() {
  const { user } = useAuth();
  const resource = useResource(
    () => Promise.all([api.subjects(), api.tasks(), api.attendanceSummary(), api.recommendations(), api.studyPlan(), api.timetable()]),
    [],
  );

  return (
    <PageState resource={resource}>
      {([subjects, tasks, attendance, recommendations, studyPlan, timetable]) => {
        const pendingTasks = tasks.filter((task) => task.status !== "Completed");
        const today = new Intl.DateTimeFormat(undefined, { weekday: "long" }).format(new Date());
        const todayEntries = timetable.filter((entry) => entry.day_of_week === today);
        return (
          <>
            <PageHeader eyebrow="Student workspace" title={`Good morning, ${user.username}.`} description="A clear view of what needs your attention next." action={<Link className="button button-primary" to="/study-plan">Open study plan</Link>} />
            <div className="stats-grid">
              <StatCard label="Overall attendance" value={`${attendance.overall_percentage}%`} detail={`${attendance.total_classes_attended}/${attendance.total_classes_conducted || 0} classes attended`} tone={attendance.overall_percentage < 75 ? "rose" : "blue"} />
              <StatCard label="Active subjects" value={subjects.length} detail="Keep your syllabus organized" tone="violet" />
              <StatCard label="Open tasks" value={pendingTasks.length} detail="Small consistent steps compound" tone="amber" />
              <StatCard label="Study plan blocks" value={studyPlan.plan.length} detail="Built from your current signals" tone="green" />
            </div>
            <div className="dashboard-grid">
              <Card className="span-two">
                <div className="section-heading"><div><p className="eyebrow">Focus queue</p><h2>What deserves attention</h2></div><Link to="/tasks">View tasks</Link></div>
                {pendingTasks.length === 0 ? <EmptyState title="Your task list is clear" description="Add a task when your next academic commitment is ready." action={<Link className="button button-secondary" to="/tasks">Add a task</Link>} /> : (
                  <div className="compact-list">{pendingTasks.slice(0, 5).map((task) => <div className="list-row" key={task.id}><div><strong>{task.title}</strong><span>{task.deadline ? `Due ${formatDate(task.deadline)}` : "No deadline"}</span></div><span className={`badge badge-${task.priority.toLowerCase()}`}>{task.priority}</span></div>)}</div>
                )}
              </Card>
              <Card>
                <div className="section-heading"><div><p className="eyebrow">Today</p><h2>{today}</h2></div><Link to="/timetable">Schedule</Link></div>
                {todayEntries.length === 0 ? <EmptyState title="No classes scheduled" description="Your day is open, or add your timetable to see it here." /> : <div className="compact-list">{todayEntries.map((entry) => <div className="list-row" key={entry.id}><div><strong>{entry.start_time} - {entry.end_time}</strong><span>{subjects.find((subject) => subject.id === entry.subject_id)?.name || "Subject"}</span></div><span className="muted">{entry.room_number || "—"}</span></div>)}</div>}
              </Card>
              <Card>
                <div className="section-heading"><div><p className="eyebrow">Signals</p><h2>Recommendations</h2></div><Link to="/recommendations">See all</Link></div>
                <div className="recommendation-list">{recommendations.recommendations.slice(0, 3).map((item) => <div className="recommendation-item" key={item}><span className="recommendation-dot">✦</span><p>{item}</p></div>)}</div>
              </Card>
              <Card className="span-two">
                <div className="section-heading"><div><p className="eyebrow">Learning profile</p><h2>Weak topics to revisit</h2></div><Link to="/quizzes">Practice</Link></div>
                {recommendations.weak_topics.length === 0 ? <EmptyState title="Your profile is still forming" description="Complete a quiz attempt to start seeing topic-level signals." /> : <div className="topic-grid">{recommendations.weak_topics.slice(0, 4).map((topic) => <div className="topic-card" key={topic.topic_id}><div><strong>{topic.topic_name}</strong><span>{topic.attempts} attempt{topic.attempts === 1 ? "" : "s"}</span></div><div className="topic-score"><b>{topic.average_score}%</b><ProgressBar value={topic.average_score} /></div></div>)}</div>}
              </Card>
            </div>
          </>
        );
      }}
    </PageState>
  );
}

export function SubjectsPage() {
  const { subjectId } = useParams();
  const navigate = useNavigate();
  const resource = useResource(() => api.subjects(), []);
  const [modal, setModal] = useState(null);
  const [name, setName] = useState("");
  const [topicName, setTopicName] = useState("");
  const [topics, setTopics] = useState([]);
  const [message, setMessage] = useState("");
  const selected = resource.data?.find((subject) => String(subject.id) === subjectId);

  useEffect(() => {
    if (!selected) { setTopics([]); return; }
    api.topics(selected.id).then(setTopics).catch((error) => setMessage(error.message));
  }, [selected?.id]);

  async function saveSubject(event) {
    event.preventDefault();
    try {
      if (modal?.type === "edit") await api.updateSubject(modal.subject.id, { name });
      else await api.createSubject({ name });
      setName(""); setModal(null); setMessage(""); resource.reload();
    } catch (error) { setMessage(error.message); }
  }

  async function removeSubject(id) {
    if (!window.confirm("Delete this subject and its topics?")) return;
    try { await api.deleteSubject(id); if (String(id) === subjectId) navigate("/subjects"); resource.reload(); } catch (error) { setMessage(error.message); }
  }

  async function saveTopic(event) {
    event.preventDefault();
    try { await api.createTopic({ name: topicName, subject_id: selected.id }); setTopicName(""); setMessage(""); setTopics(await api.topics(selected.id)); } catch (error) { setMessage(error.message); }
  }

  return (
    <PageState resource={resource}>
      {(subjects) => (
        <>
          <PageHeader eyebrow="Academic structure" title="Subjects" description="Keep your semester organized around the subjects you actually need to move forward." action={<Button onClick={() => { setName(""); setModal({ type: "create" }); }}>Add subject</Button>} />
          {message && <div className="inline-error">{message}</div>}
          {subjects.length === 0 ? <Card><EmptyState title="No subjects yet" description="Start with the first subject in your current semester." action={<Button onClick={() => setModal({ type: "create" })}>Create first subject</Button>} /></Card> : <div className="subject-layout"><div className="subject-list">{subjects.map((subject) => <Card className={`subject-card ${selected?.id === subject.id ? "selected" : ""}`} key={subject.id}><button className="subject-main" onClick={() => navigate(`/subjects/${subject.id}`)}><span className="subject-symbol">{subject.name.slice(0, 1).toUpperCase()}</span><span><strong>{subject.name}</strong><small>Subject workspace</small></span><span className="arrow">→</span></button><div className="card-actions"><button onClick={() => { setName(subject.name); setModal({ type: "edit", subject }); }}>Edit</button><button className="danger-text" onClick={() => removeSubject(subject.id)}>Delete</button></div></Card>)}</div>{selected && <Card className="subject-detail"><div className="section-heading"><div><p className="eyebrow">Subject workspace</p><h2>{selected.name}</h2></div><Link to="/topics">All topics</Link></div><form className="inline-form" onSubmit={saveTopic}><input required value={topicName} onChange={(event) => setTopicName(event.target.value)} placeholder="Add a topic" /><Button type="submit">Add topic</Button></form>{topics.length === 0 ? <EmptyState title="No topics yet" description="Break this subject into smaller concepts to make progress trackable." /> : <div className="topic-list">{topics.map((topic) => <div className="list-row" key={topic.id}><div><strong>{topic.name}</strong><span>Created {formatDate(topic.created_at)}</span></div><button className="danger-text" onClick={async () => { await api.deleteTopic(topic.id); setTopics(await api.topics(selected.id)); }}>Remove</button></div>)}</div>}</Card>}</div>}
          {modal && <Modal title={modal.type === "edit" ? "Edit subject" : "Add subject"} onClose={() => setModal(null)}><form className="stack-form" onSubmit={saveSubject}><Field label="Subject name"><input autoFocus required value={name} onChange={(event) => setName(event.target.value)} placeholder="e.g. Machine Learning" /></Field><Button type="submit">Save subject</Button></form></Modal>}
        </>
      )}
    </PageState>
  );
}

export function TopicsPage() {
  const subjectsResource = useResource(() => api.subjects(), []);
  const [selectedId, setSelectedId] = useState("");
  const topicsResource = useResource(() => selectedId ? api.topics(selectedId) : Promise.resolve([]), [selectedId]);
  const [name, setName] = useState("");
  const [error, setError] = useState("");

  async function addTopic(event) {
    event.preventDefault();
    try { await api.createTopic({ name, subject_id: Number(selectedId) }); setName(""); topicsResource.reload(); } catch (err) { setError(err.message); }
  }

  return <PageState resource={subjectsResource}>{(subjects) => <><PageHeader eyebrow="Academic structure" title="Topics" description="Turn broad subjects into focused concepts you can practice and revisit." />{subjects.length === 0 ? <Card><EmptyState title="Create a subject first" description="Topics belong to a subject. Add your first subject to get started." action={<Link className="button button-primary" to="/subjects">Go to subjects</Link>} /></Card> : <div className="two-column"><Card><Field label="Subject"><select value={selectedId} onChange={(event) => setSelectedId(event.target.value)}><option value="">Choose a subject</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select></Field><form className="inline-form" onSubmit={addTopic}><input required value={name} onChange={(event) => setName(event.target.value)} placeholder="New topic name" /><Button type="submit" disabled={!selectedId}>Add</Button></form>{error && <div className="form-error">{error}</div>}</Card><Card><p className="eyebrow">Topics in subject</p><h2>{subjects.find((subject) => String(subject.id) === String(selectedId))?.name || "Choose a subject"}</h2><PageState resource={topicsResource}>{(topics) => topics.length ? <div className="topic-list">{topics.map((topic) => <div className="list-row" key={topic.id}><strong>{topic.name}</strong><button className="danger-text" onClick={async () => { await api.deleteTopic(topic.id); topicsResource.reload(); }}>Delete</button></div>)}</div> : <EmptyState title="Nothing mapped yet" description="Add a topic to see it here." />}</PageState></Card></div>}</>}{/* */}</PageState>;
}

export function TasksPage() {
  const resource = useResource(() => Promise.all([api.tasks(), api.subjects()]), []);
  const [topics, setTopics] = useState([]);
  const [form, setForm] = useState({ title: "", description: "", priority: "Medium", status: "Pending", deadline: "", topic_id: "" });
  const [error, setError] = useState("");
  useEffect(() => { if (resource.data?.[1]) Promise.all(resource.data[1].map((subject) => api.topics(subject.id))).then((groups) => setTopics(groups.flat())); }, [resource.data]);
  async function create(event) {
    event.preventDefault();
    try { await api.createTask({ ...form, topic_id: Number(form.topic_id), deadline: form.deadline || null }); setForm({ title: "", description: "", priority: "Medium", status: "Pending", deadline: "", topic_id: "" }); resource.reload(); } catch (err) { setError(err.message); }
  }
  async function updateStatus(task, status) {
    try { await api.updateTask(task.id, { status }); resource.reload(); } catch (err) { setError(err.message); }
  }
  return <PageState resource={resource}>{([tasks, subjects]) => <><PageHeader eyebrow="Execution" title="Tasks" description="Turn your syllabus into small, visible commitments." /><div className="two-column"><Card><div className="section-heading"><div><p className="eyebrow">New task</p><h2>Add commitment</h2></div></div><form className="stack-form" onSubmit={create}><Field label="Title"><input required value={form.title} onChange={(event) => setForm({ ...form, title: event.target.value })} placeholder="Finish practice set" /></Field><Field label="Topic"><select required value={form.topic_id} onChange={(event) => setForm({ ...form, topic_id: event.target.value })}><option value="">Choose a topic</option>{topics.map((topic) => <option key={topic.id} value={topic.id}>{topic.name}</option>)}</select></Field><div className="form-grid"><Field label="Priority"><select value={form.priority} onChange={(event) => setForm({ ...form, priority: event.target.value })}><option>Low</option><option>Medium</option><option>High</option></select></Field><Field label="Deadline"><input type="datetime-local" value={form.deadline} onChange={(event) => setForm({ ...form, deadline: event.target.value })} /></Field></div><Field label="Description"><textarea value={form.description} onChange={(event) => setForm({ ...form, description: event.target.value })} placeholder="What does done look like?" /></Field>{error && <div className="form-error">{error}</div>}<Button type="submit" disabled={!topics.length}>Create task</Button></form></Card><Card><div className="section-heading"><div><p className="eyebrow">Task queue</p><h2>{tasks.length} task{tasks.length === 1 ? "" : "s"}</h2></div></div>{tasks.length === 0 ? <EmptyState title="Your queue is empty" description="Create a task tied to a topic to start building momentum." /> : <div className="task-list">{tasks.map((task) => <div className="task-row" key={task.id}><div className="task-check"><input type="checkbox" checked={task.status === "Completed"} onChange={(event) => updateStatus(task, event.target.checked ? "Completed" : "Pending")} /><div><strong className={task.status === "Completed" ? "completed" : ""}>{task.title}</strong><span>{task.deadline ? `Due ${formatDate(task.deadline)}` : "No deadline"} · {task.priority} priority</span></div></div><button className="danger-text" onClick={async () => { await api.deleteTask(task.id); resource.reload(); }}>Delete</button></div>)}</div>}</Card></div></>}</PageState>;
}

const DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"];
export function TimetablePage() {
  const resource = useResource(() => Promise.all([api.timetable(), api.subjects()]), []);
  const [form, setForm] = useState({ subject_id: "", day_of_week: "Monday", start_time: "09:00", end_time: "10:00", room_number: "" });
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    try { await api.createTimetable({ ...form, subject_id: Number(form.subject_id) }); resource.reload(); setError(""); } catch (err) { setError(err.message); }
  }
  return <PageState resource={resource}>{([entries, subjects]) => <><PageHeader eyebrow="Weekly rhythm" title="Timetable" description="Make your available learning time visible before the week fills up." /><div className="two-column timetable-layout"><Card><p className="eyebrow">Add class</p><h2>Schedule a slot</h2><form className="stack-form" onSubmit={submit}><Field label="Subject"><select required value={form.subject_id} onChange={(event) => setForm({ ...form, subject_id: event.target.value })}><option value="">Choose a subject</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select></Field><Field label="Day"><select value={form.day_of_week} onChange={(event) => setForm({ ...form, day_of_week: event.target.value })}>{DAYS.map((day) => <option key={day}>{day}</option>)}</select></Field><div className="form-grid"><Field label="Starts"><input type="time" required value={form.start_time} onChange={(event) => setForm({ ...form, start_time: event.target.value })} /></Field><Field label="Ends"><input type="time" required value={form.end_time} onChange={(event) => setForm({ ...form, end_time: event.target.value })} /></Field></div><Field label="Room"><input value={form.room_number} onChange={(event) => setForm({ ...form, room_number: event.target.value })} placeholder="Optional" /></Field>{error && <div className="form-error">{error}</div>}<Button type="submit">Add to timetable</Button></form></Card><div className="week-grid">{DAYS.map((day) => <Card key={day} className="day-column"><div className="day-heading"><strong>{day.slice(0, 3)}</strong><span>{entries.filter((entry) => entry.day_of_week === day).length}</span></div>{entries.filter((entry) => entry.day_of_week === day).map((entry) => <div className="schedule-entry" key={entry.id}><strong>{subjects.find((subject) => subject.id === entry.subject_id)?.name || "Subject"}</strong><span>{entry.start_time} - {entry.end_time}</span><small>{entry.room_number || "No room"}</small><button className="danger-text" onClick={async () => { await api.deleteTimetable(entry.id); resource.reload(); }}>Remove</button></div>)}{entries.filter((entry) => entry.day_of_week === day).length === 0 && <span className="muted day-empty">Open</span>}</Card>)}</div></div></>}</PageState>;
}

export function AttendancePage() {
  const resource = useResource(() => Promise.all([api.attendanceSummary(), api.attendanceLogs(), api.subjects()]), []);
  const [form, setForm] = useState({ subject_id: "", date: new Date().toISOString().slice(0, 10), status: "Present", notes: "" });
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault();
    try { await api.createAttendance({ ...form, subject_id: Number(form.subject_id) }); resource.reload(); } catch (err) { setError(err.message); }
  }
  return <PageState resource={resource}>{([summary, logs, subjects]) => <><PageHeader eyebrow="Consistency" title="Attendance" description="See where your attendance stands and record each class with confidence." /><div className="stats-grid"><StatCard label="Overall" value={`${summary.overall_percentage}%`} detail={`${summary.total_classes_attended} attended`} tone={summary.overall_percentage < 75 ? "rose" : "green"} /><StatCard label="Classes conducted" value={summary.total_classes_conducted} detail="Cancelled sessions excluded" tone="blue" /><StatCard label="Subjects tracked" value={summary.subjects_stats.length} detail="Across your workspace" tone="violet" /></div><div className="two-column"><Card><p className="eyebrow">Record a class</p><h2>Mark attendance</h2><form className="stack-form" onSubmit={submit}><Field label="Subject"><select required value={form.subject_id} onChange={(event) => setForm({ ...form, subject_id: event.target.value })}><option value="">Choose a subject</option>{subjects.map((subject) => <option key={subject.id} value={subject.id}>{subject.name}</option>)}</select></Field><div className="form-grid"><Field label="Date"><input type="date" required value={form.date} onChange={(event) => setForm({ ...form, date: event.target.value })} /></Field><Field label="Status"><select value={form.status} onChange={(event) => setForm({ ...form, status: event.target.value })}><option>Present</option><option>Absent</option><option>Cancelled</option></select></Field></div><Field label="Notes"><textarea value={form.notes} onChange={(event) => setForm({ ...form, notes: event.target.value })} placeholder="Optional note" /></Field>{error && <div className="form-error">{error}</div>}<Button type="submit">Save attendance</Button></form></Card><Card><p className="eyebrow">Subject health</p><h2>Attendance by subject</h2>{summary.subjects_stats.length === 0 ? <EmptyState title="No attendance yet" description="Record a class to start seeing subject-level signals." /> : <div className="attendance-list">{summary.subjects_stats.map((stat) => <div className="attendance-row" key={stat.subject_id}><div><strong>{stat.subject_name}</strong><span>{stat.total_attended}/{stat.total_conducted || 0} attended</span></div><div className="attendance-value"><b>{stat.percentage}%</b><ProgressBar value={stat.percentage} /></div></div>)}</div>}</Card></div><Card><div className="section-heading"><div><p className="eyebrow">History</p><h2>Recent attendance</h2></div></div>{logs.length === 0 ? <EmptyState title="No logs yet" description="Your recent attendance records will appear here." /> : <div className="table-wrap"><table><thead><tr><th>Date</th><th>Subject</th><th>Status</th><th>Notes</th></tr></thead><tbody>{logs.slice(0, 20).map((log) => <tr key={log.id}><td>{formatDate(log.date)}</td><td>{subjects.find((subject) => subject.id === log.subject_id)?.name || "Subject"}</td><td><span className={`badge badge-${log.status.toLowerCase()}`}>{log.status}</span></td><td>{log.notes || "—"}</td></tr>)}</tbody></table></div>}</Card></>}</PageState>;
}

export function MaterialsPage() {
  const resource = useResource(() => api.materials(), []);
  const [file, setFile] = useState(null);
  const [title, setTitle] = useState("");
  const [error, setError] = useState("");
  const [uploading, setUploading] = useState(false);
  async function submit(event) {
    event.preventDefault();
    if (!file) return;
    setUploading(true); setError("");
    try { await api.uploadMaterial(file, title); setFile(null); setTitle(""); event.target.reset(); resource.reload(); } catch (err) { setError(err.message); } finally { setUploading(false); }
  }
  return <PageState resource={resource}>{(materials) => <><PageHeader eyebrow="Study library" title="Materials" description="Upload your own notes and ask grounded questions against the extracted content." /><div className="two-column"><Card><p className="eyebrow">Upload</p><h2>Add study material</h2><form className="stack-form" onSubmit={submit}><Field label="Title"><input value={title} onChange={(event) => setTitle(event.target.value)} placeholder="Operating Systems notes" /></Field><Field label="File" hint="TXT, Markdown, and PDF up to 5 MB"><input required type="file" accept=".txt,.md,.pdf" onChange={(event) => setFile(event.target.files[0])} /></Field>{error && <div className="form-error">{error}</div>}<Button type="submit" disabled={!file || uploading}>{uploading ? "Processing..." : "Upload material"}</Button></form></Card><Card><p className="eyebrow">Library</p><h2>{materials.length} material{materials.length === 1 ? "" : "s"}</h2>{materials.length === 0 ? <EmptyState title="Your library is empty" description="Upload a PDF, TXT, or Markdown file to begin." /> : <div className="material-list">{materials.map((material) => <Link to={`/materials/${material.id}`} className="material-row" key={material.id}><span className="file-icon">▤</span><div><strong>{material.title}</strong><span>{material.original_filename} · {material.status}</span></div><span>→</span></Link>)}</div>}</Card></div></>}</PageState>;
}

export function MaterialDetailPage() {
  const { documentId } = useParams();
  const resource = useResource(() => api.material(documentId), [documentId]);
  const [question, setQuestion] = useState("");
  const [answer, setAnswer] = useState(null);
  const [artifact, setArtifact] = useState(null);
  const [error, setError] = useState("");
  const [busy, setBusy] = useState(false);
  async function ask(event) {
    event.preventDefault(); setBusy(true); setError("");
    try { setAnswer(await api.askMaterial(documentId, question)); setQuestion(""); } catch (err) { setError(err.message); } finally { setBusy(false); }
  }
  async function generate(type) {
    setBusy(true); setError("");
    try { setArtifact(await api.generateMaterial(documentId, type)); } catch (err) { setError(err.message); } finally { setBusy(false); }
  }
  return <PageState resource={resource}>{(material) => <><PageHeader eyebrow="Study material" title={material.title} description={`${material.original_filename} · ${material.status}`} action={<Link className="button button-secondary" to="/materials">Back to library</Link>} />{error && <div className="inline-error">{error}</div>}<div className="two-column"><Card><p className="eyebrow">Ask your material</p><h2>Grounded questions</h2><form className="stack-form" onSubmit={ask}><Field label="Question"><textarea required value={question} onChange={(event) => setQuestion(event.target.value)} placeholder="What is the main idea in this document?" /></Field><Button type="submit" disabled={busy}>{busy ? "Searching..." : "Ask question"}</Button></form>{answer && <div className="answer-box"><span className="eyebrow">Answer</span><p>{answer.answer}</p>{answer.relevant_chunks?.length > 0 && <details><summary>Relevant extracted chunks</summary>{answer.relevant_chunks.map((chunk, index) => <p className="source-chip" key={index}>{chunk}</p>)}</details>}</div>}</Card><Card><p className="eyebrow">Study tools</p><h2>Create a quick artifact</h2><p className="muted">These tools use the current backend's extracted text and deterministic scaffolding.</p><div className="tool-grid">{[["summary", "Summary"], ["notes", "Notes"], ["mcqs", "MCQs"], ["flashcards", "Flashcards"], ["important_questions", "Important questions"]].map(([type, label]) => <button className="tool-button" key={type} onClick={() => generate(type)} disabled={busy}><strong>{label}</strong><span>Generate →</span></button>)}</div>{artifact && <div className="answer-box"><span className="eyebrow">{artifact.title}</span><pre>{artifact.content}</pre></div>}</Card></div></>}</PageState>;
}

export function QuizzesPage() {
  const resource = useResource(() => Promise.all([api.subjects(), api.quizAttempts(), api.weakTopics()]), []);
  const [topics, setTopics] = useState([]);
  const [selectedTopic, setSelectedTopic] = useState("");
  const questionsResource = useResource(() => selectedTopic ? api.quizQuestions(selectedTopic) : Promise.resolve([]), [selectedTopic]);
  const [answers, setAnswers] = useState({});
  const [result, setResult] = useState(null);
  const [questionForm, setQuestionForm] = useState({ question_text: "", option_a: "", option_b: "", option_c: "", option_d: "", correct_option: "A", difficulty: "Medium" });
  const [error, setError] = useState("");
  useEffect(() => { if (resource.data?.[0]) Promise.all(resource.data[0].map((subject) => api.topics(subject.id))).then((groups) => setTopics(groups.flat())); }, [resource.data]);
  async function submitQuiz(event) {
    event.preventDefault(); setError("");
    try { setResult(await api.submitQuiz({ topic_id: Number(selectedTopic), answers })); resource.reload(); setAnswers({}); } catch (err) { setError(err.message); }
  }
  async function createQuestion(event) {
    event.preventDefault(); setError("");
    try { await api.createQuizQuestion({ ...questionForm, topic_id: Number(selectedTopic) }); setQuestionForm({ question_text: "", option_a: "", option_b: "", option_c: "", option_d: "", correct_option: "A", difficulty: "Medium" }); questionsResource.reload(); } catch (err) { setError(err.message); }
  }
  return <PageState resource={resource}>{([subjects, attempts, weakTopics]) => <><PageHeader eyebrow="Practice loop" title="Quizzes" description="Practice from your own question bank, then use the result to guide your next revision block." /><Card><Field label="Choose a topic"><select value={selectedTopic} onChange={(event) => { setSelectedTopic(event.target.value); setResult(null); }}><option value="">Choose a topic</option>{topics.map((topic) => <option key={topic.id} value={topic.id}>{topic.name}</option>)}</select></Field>{error && <div className="form-error">{error}</div>}</Card>{selectedTopic && <div className="two-column"><Card><div className="section-heading"><div><p className="eyebrow">Question set</p><h2>Attempt quiz</h2></div></div><PageState resource={questionsResource}>{(questions) => questions.length === 0 ? <EmptyState title="No questions yet" description="Add the first question for this topic in the panel beside this one." /> : <form onSubmit={submitQuiz}><div className="quiz-list">{questions.map((question, index) => <div className="quiz-question" key={question.id}><p className="question-number">Question {index + 1}</p><h3>{question.question_text}</h3>{["A", "B", "C", "D"].map((option) => <label className={`option ${answers[question.id] === option ? "selected" : ""}`} key={option}><input type="radio" name={`question-${question.id}`} value={option} checked={answers[question.id] === option} onChange={() => setAnswers({ ...answers, [question.id]: option })} />{option}. {question[`option_${option.toLowerCase()}`]}</label>)}</div>)}</div><Button type="submit" disabled={Object.keys(answers).length !== questions.length}>Submit attempt</Button></form>}</PageState>{result && <div className="result-banner"><strong>{result.percentage}%</strong><span>{result.questions_correct} of {result.questions_total} correct</span></div>}</Card><Card><p className="eyebrow">Build your bank</p><h2>Add question</h2><form className="stack-form" onSubmit={createQuestion}><Field label="Question"><textarea required value={questionForm.question_text} onChange={(event) => setQuestionForm({ ...questionForm, question_text: event.target.value })} /></Field>{["a", "b", "c", "d"].map((option) => <Field label={`Option ${option.toUpperCase()}`} key={option}><input required value={questionForm[`option_${option}`]} onChange={(event) => setQuestionForm({ ...questionForm, [`option_${option}`]: event.target.value })} /></Field>)}<div className="form-grid"><Field label="Correct option"><select value={questionForm.correct_option} onChange={(event) => setQuestionForm({ ...questionForm, correct_option: event.target.value })}><option>A</option><option>B</option><option>C</option><option>D</option></select></Field><Field label="Difficulty"><select value={questionForm.difficulty} onChange={(event) => setQuestionForm({ ...questionForm, difficulty: event.target.value })}><option>Easy</option><option>Medium</option><option>Hard</option></select></Field></div><Button type="submit">Add question</Button></form></Card></div>}<div className="two-column"><Card><p className="eyebrow">Weak topics</p><h2>Where to revisit</h2>{weakTopics.length === 0 ? <EmptyState title="No weak topics yet" description="Submit a quiz attempt to build your learning profile." /> : <div className="topic-list">{weakTopics.map((topic) => <div className="list-row" key={topic.topic_id}><div><strong>{topic.topic_name}</strong><span>{topic.attempts} attempt{topic.attempts === 1 ? "" : "s"}</span></div><strong>{topic.average_score}%</strong></div>)}</div>}</Card><Card><p className="eyebrow">History</p><h2>Recent attempts</h2>{attempts.length === 0 ? <EmptyState title="No attempts yet" description="Your submitted quizzes will appear here." /> : <div className="topic-list">{attempts.slice(0, 8).map((attempt) => <div className="list-row" key={attempt.id}><div><strong>{attempt.questions_correct}/{attempt.questions_total} correct</strong><span>{formatDate(attempt.submitted_at)}</span></div><strong>{attempt.percentage}%</strong></div>)}</div>}</Card></div></>}</PageState>;
}

export function RecommendationsPage() {
  const resource = useResource(() => api.recommendations(), []);
  return <PageState resource={resource}>{(data) => <><PageHeader eyebrow="Learning signals" title="Recommendations" description="Personalized guidance based on the attendance and quiz data currently in your workspace." /><div className="stats-grid"><StatCard label="Overall attendance" value={`${data.overall_attendance}%`} detail="Current deterministic summary" tone={data.overall_attendance < 75 ? "rose" : "green"} /><StatCard label="Topics needing attention" value={data.weak_topics.filter((topic) => topic.status !== "Strong").length} detail="Based on quiz attempts" tone="amber" /></div><Card><div className="recommendation-list large">{data.recommendations.map((item, index) => <div className="recommendation-item" key={item}><span className="recommendation-index">0{index + 1}</span><p>{item}</p></div>)}</div></Card><Card><p className="eyebrow">Evidence</p><h2>Topic performance</h2>{data.weak_topics.length === 0 ? <EmptyState title="No topic evidence yet" description="Complete quizzes to make recommendations more specific." /> : <div className="topic-grid">{data.weak_topics.map((topic) => <div className="topic-card" key={topic.topic_id}><div><strong>{topic.topic_name}</strong><span>{topic.status} · {topic.attempts} attempts</span></div><div className="topic-score"><b>{topic.average_score}%</b><ProgressBar value={topic.average_score} /></div></div>)}</div>}</Card></>}</PageState>;
}

export function StudyPlanPage() {
  const resource = useResource(() => api.studyPlan(), []);
  return <PageState resource={resource}>{(data) => <><PageHeader eyebrow="Plan your week" title="Study plan" description="A deterministic baseline plan shaped by your current weak-topic signals." /><div className="plan-banner"><div><p className="eyebrow">Focus areas</p><h2>{data.focus_areas.join(" · ")}</h2></div><span className="plan-mark">◷</span></div><div className="plan-list">{data.plan.map((item) => <Card className="plan-card" key={item.day}><div className="plan-day">0{item.day}<span>DAY</span></div><div className="plan-content"><p className="eyebrow">Study block</p><h2>{item.topic}</h2><p>{item.focus}</p></div><div className="plan-duration"><strong>{item.duration_minutes}</strong><span>minutes</span></div></Card>)}</div></>}</PageState>;
}

export function ProfilePage() {
  const { user } = useAuth();
  return <><PageHeader eyebrow="Account" title="Profile" description="Your academic identity in LearnMate AI." /><Card className="profile-card"><div className="profile-avatar">{user.username.slice(0, 1).toUpperCase()}</div><div><p className="eyebrow">Student profile</p><h2>{user.username}</h2><p className="muted">{user.email}</p></div></Card><div className="profile-grid"><Card><span className="muted">College</span><strong>{user.college?.name || "Not added yet"}</strong><p>{user.college?.email_domain || "Add this from your account settings when available."}</p></Card><Card><span className="muted">Branch</span><strong>{user.branch?.name || "Not added yet"}</strong><p>{user.branch?.code || "Academic branch not selected."}</p></Card><Card><span className="muted">Semester</span><strong>Semester {user.semester}</strong><p>Keep your current term visible as your workspace grows.</p></Card></div></>;
}

export function PredictionsPage() {
  const [form, setForm] = useState({ study_hours: 0, revision_hours: 0, attendance: 75, quiz_score: 0, mock_test_score: 0, assignments_completed: 0 });
  const [result, setResult] = useState(null);
  const [error, setError] = useState("");
  async function submit(event) {
    event.preventDefault(); setError("");
    try { setResult(await api.predict({ ...form, study_hours: Number(form.study_hours), revision_hours: Number(form.revision_hours), attendance: Number(form.attendance), quiz_score: Number(form.quiz_score), mock_test_score: Number(form.mock_test_score), assignments_completed: Number(form.assignments_completed) })); } catch (err) { setError(err.message); }
  }
  return <><PageHeader eyebrow="Transparent baseline" title="Performance baseline" description="A deterministic baseline from the current API, not a trained ML forecast." /><div className="two-column"><Card><form className="stack-form" onSubmit={submit}>{[["study_hours", "Study hours"], ["revision_hours", "Revision hours"], ["attendance", "Attendance %"], ["quiz_score", "Quiz score"], ["mock_test_score", "Mock test score"], ["assignments_completed", "Assignments completed"]].map(([key, label]) => <Field label={label} key={key}><input type="number" min="0" max={key === "attendance" || key.includes("score") ? 100 : undefined} value={form[key]} onChange={(event) => setForm({ ...form, [key]: event.target.value })} /></Field>)}{error && <div className="form-error">{error}</div>}<Button type="submit">Calculate baseline</Button></form></Card><Card>{result ? <><p className="eyebrow">Result</p><div className="baseline-score">{result.predicted_score}<span>/ 100</span></div><p className="muted">This value is the current deterministic baseline returned by the backend.</p><div className="recommendation-list">{result.recommendations.map((item) => <div className="recommendation-item" key={item}><span className="recommendation-dot">✦</span><p>{item}</p></div>)}</div></> : <EmptyState title="No baseline calculated" description="Enter the learning signals available to you and calculate a transparent baseline." />}</Card></div></>;
}
