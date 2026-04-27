import React, { useEffect, useMemo, useState } from "react";

const DEFAULT_PROFILE = {
  name: "Marco",
  level: "beginner",
  dailyMinutes: 15,
  focus: "work",
  nativeLanguage: "pt-BR",
};

const LESSON_BANK = [
  {
    id: 1,
    category: "survival",
    difficulty: 1,
    theme: "Pedidos básicos",
    english: "Can you help me?",
    portuguese: "Você pode me ajudar?",
    prompt: "Imagine que você precisa pedir ajuda em um local desconhecido.",
    variations: ["I need help.", "Please help me.", "Could you help me?"],
  },
  {
    id: 2,
    category: "survival",
    difficulty: 1,
    theme: "Entendimento",
    english: "I don't understand.",
    portuguese: "Eu não entendo.",
    prompt: "Use quando alguém falar rápido demais.",
    variations: ["Can you repeat?", "Please speak slowly.", "Say that again, please."],
  },
  {
    id: 3,
    category: "conversation",
    difficulty: 1,
    theme: "Apresentação",
    english: "My name is Marco. I live in Brazil.",
    portuguese: "Meu nome é Marco. Eu moro no Brasil.",
    prompt: "Apresente-se de forma simples.",
    variations: ["I am from Brazil.", "I work in IT.", "Nice to meet you."],
  },
  {
    id: 4,
    category: "work",
    difficulty: 2,
    theme: "Reuniões",
    english: "Let me check and get back to you.",
    portuguese: "Deixe-me verificar e retorno para você.",
    prompt: "Use em contexto profissional quando precisar confirmar uma informação.",
    variations: ["I will review this.", "I need a few minutes.", "I will update you soon."],
  },
  {
    id: 5,
    category: "work",
    difficulty: 2,
    theme: "Rotina profissional",
    english: "I work with data, processes, and service quality.",
    portuguese: "Eu trabalho com dados, processos e qualidade de serviços.",
    prompt: "Fale sobre seu trabalho de forma objetiva.",
    variations: ["I work in IT.", "I improve processes.", "I create reports and indicators."],
  },
  {
    id: 6,
    category: "conversation",
    difficulty: 2,
    theme: "Tempo",
    english: "I don't have much time, but I study every day.",
    portuguese: "Eu não tenho muito tempo, mas estudo todos os dias.",
    prompt: "Explique sua rotina com sinceridade.",
    variations: ["My routine is busy.", "I study for 15 minutes a day.", "Consistency is important."],
  },
  {
    id: 7,
    category: "travel",
    difficulty: 2,
    theme: "Direções",
    english: "Where is the bathroom?",
    portuguese: "Onde fica o banheiro?",
    prompt: "Use em um aeroporto, restaurante ou shopping.",
    variations: ["Where is the exit?", "How do I get there?", "Is it far from here?"],
  },
  {
    id: 8,
    category: "work",
    difficulty: 3,
    theme: "Opinião profissional",
    english: "In my opinion, we need a clearer process and better communication.",
    portuguese: "Na minha opinião, precisamos de um processo mais claro e de melhor comunicação.",
    prompt: "Dê uma opinião em uma reunião de trabalho.",
    variations: ["I see an opportunity for improvement.", "We need to reduce rework.", "This can improve efficiency."],
  },
  {
    id: 9,
    category: "conversation",
    difficulty: 3,
    theme: "Objetivos",
    english: "I am learning English to communicate confidently.",
    portuguese: "Estou aprendendo inglês para me comunicar com confiança.",
    prompt: "Explique sua motivação.",
    variations: ["I want to speak naturally.", "I want to understand more.", "I am improving step by step."],
  },
  {
    id: 10,
    category: "work",
    difficulty: 3,
    theme: "Alinhamento",
    english: "Could we align expectations before starting the project?",
    portuguese: "Podemos alinhar as expectativas antes de começar o projeto?",
    prompt: "Use em um contexto de gestão de projetos.",
    variations: ["Let's define the next steps.", "We need clear priorities.", "Who is responsible for this task?"],
  },
];

function todayKey() {
  const d = new Date();
  return `${d.getFullYear()}-${String(d.getMonth() + 1).padStart(2, "0")}-${String(d.getDate()).padStart(2, "0")}`;
}

function loadFromStorage(key, fallback) {
  try {
    const raw = localStorage.getItem(key);
    return raw ? JSON.parse(raw) : fallback;
  } catch {
    return fallback;
  }
}

function saveToStorage(key, value) {
  localStorage.setItem(key, JSON.stringify(value));
}

function scoreLabel(score) {
  if (score >= 85) return "Excelente";
  if (score >= 65) return "Bom";
  if (score >= 40) return "Em evolução";
  return "Começando";
}

function getAdaptiveLessons(profile, progress) {
  const stats = progress.lessonStats || {};
  const preferredCategory =
    profile.focus === "travel" ? "travel" : profile.focus === "work" ? "work" : "conversation";

  const unseen = LESSON_BANK.filter((lesson) => !stats[lesson.id]);
  const weak = LESSON_BANK.filter((lesson) => stats[lesson.id] && stats[lesson.id].mastery < 70);
  const medium = LESSON_BANK.filter(
    (lesson) => stats[lesson.id] && stats[lesson.id].mastery >= 70 && stats[lesson.id].mastery < 90
  );

  const prioritized = [
    ...weak.filter((l) => l.category === preferredCategory),
    ...weak.filter((l) => l.category !== preferredCategory),
    ...unseen.filter((l) => l.category === preferredCategory),
    ...unseen.filter((l) => l.category !== preferredCategory),
    ...medium,
  ];

  const unique = Array.from(new Map(prioritized.map((item) => [item.id, item])).values());
  const dailyCount = profile.dailyMinutes <= 10 ? 2 : profile.dailyMinutes <= 20 ? 3 : 4;
  return unique.slice(0, dailyCount);
}

const styles = {
  page: {
    minHeight: "100vh",
    background: "linear-gradient(180deg, #f8fafc 0%, #eef2ff 100%)",
    color: "#0f172a",
    fontFamily:
      'Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
    padding: "24px",
    boxSizing: "border-box",
  },
  container: {
    maxWidth: "1180px",
    margin: "0 auto",
  },
  heroGrid: {
    display: "grid",
    gridTemplateColumns: "2fr 1fr",
    gap: "16px",
    marginBottom: "16px",
  },
  card: {
    background: "#ffffff",
    borderRadius: "24px",
    padding: "24px",
    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.08)",
    border: "1px solid rgba(148, 163, 184, 0.18)",
  },
  title: {
    margin: 0,
    fontSize: "34px",
    lineHeight: 1.1,
  },
  subtitle: {
    color: "#475569",
    marginTop: "10px",
    marginBottom: 0,
    fontSize: "16px",
  },
  badge: {
    display: "inline-block",
    background: "#e2e8f0",
    color: "#0f172a",
    padding: "8px 12px",
    borderRadius: "999px",
    fontSize: "13px",
    fontWeight: 600,
  },
  statsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(4, 1fr)",
    gap: "12px",
    marginTop: "20px",
  },
  statBox: {
    background: "#f8fafc",
    borderRadius: "18px",
    padding: "16px",
  },
  label: {
    fontSize: "13px",
    color: "#64748b",
    marginBottom: "8px",
  },
  statValue: {
    fontSize: "30px",
    fontWeight: 800,
    lineHeight: 1,
    marginBottom: "6px",
  },
  statHelp: {
    fontSize: "13px",
    color: "#64748b",
  },
  field: {
    display: "flex",
    flexDirection: "column",
    gap: "8px",
    marginBottom: "14px",
  },
  fieldLabel: {
    fontSize: "14px",
    fontWeight: 700,
  },
  input: {
    width: "100%",
    boxSizing: "border-box",
    padding: "12px 14px",
    borderRadius: "14px",
    border: "1px solid #cbd5e1",
    fontSize: "15px",
    outline: "none",
    background: "#fff",
  },
  tabs: {
    display: "flex",
    gap: "8px",
    background: "#ffffff",
    padding: "8px",
    borderRadius: "20px",
    boxShadow: "0 10px 30px rgba(15, 23, 42, 0.06)",
    border: "1px solid rgba(148, 163, 184, 0.18)",
    marginBottom: "16px",
    flexWrap: "wrap",
  },
  tabButton: {
    border: 0,
    borderRadius: "14px",
    padding: "12px 16px",
    cursor: "pointer",
    background: "transparent",
    fontWeight: 700,
    fontSize: "14px",
  },
  activeTabButton: {
    background: "#0f172a",
    color: "#ffffff",
  },
  progressWrap: {
    background: "#e2e8f0",
    borderRadius: "999px",
    height: "12px",
    overflow: "hidden",
  },
  progressBar: {
    height: "100%",
    background: "linear-gradient(90deg, #2563eb 0%, #7c3aed 100%)",
    borderRadius: "999px",
  },
  lessonsList: {
    display: "grid",
    gap: "16px",
  },
  lessonGrid: {
    display: "grid",
    gridTemplateColumns: "1.1fr 0.9fr",
    gap: "18px",
    alignItems: "start",
  },
  pillRow: {
    display: "flex",
    flexWrap: "wrap",
    gap: "8px",
    marginBottom: "14px",
  },
  pill: {
    display: "inline-block",
    background: "#eff6ff",
    color: "#1d4ed8",
    border: "1px solid #bfdbfe",
    padding: "7px 10px",
    borderRadius: "999px",
    fontSize: "12px",
    fontWeight: 700,
  },
  english: {
    fontSize: "28px",
    fontWeight: 800,
    lineHeight: 1.2,
    marginBottom: "16px",
  },
  box: {
    background: "#f8fafc",
    borderRadius: "18px",
    padding: "16px",
    border: "1px solid #e2e8f0",
    marginBottom: "14px",
  },
  textarea: {
    width: "100%",
    minHeight: "120px",
    boxSizing: "border-box",
    padding: "12px 14px",
    borderRadius: "14px",
    border: "1px solid #cbd5e1",
    fontSize: "15px",
    resize: "vertical",
    outline: "none",
    background: "#fff",
  },
  actionRow: {
    display: "flex",
    gap: "12px",
    flexWrap: "wrap",
    marginTop: "16px",
  },
  button: {
    border: 0,
    borderRadius: "16px",
    padding: "14px 18px",
    fontWeight: 800,
    fontSize: "14px",
    cursor: "pointer",
    background: "#0f172a",
    color: "#ffffff",
  },
  secondaryButton: {
    background: "#ffffff",
    color: "#0f172a",
    border: "1px solid #cbd5e1",
  },
  dangerButton: {
    background: "#b91c1c",
    color: "#ffffff",
  },
  twoCols: {
    display: "grid",
    gridTemplateColumns: "1fr 1fr",
    gap: "16px",
  },
  historyItem: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    gap: "12px",
    background: "#f8fafc",
    borderRadius: "18px",
    padding: "14px 16px",
    marginBottom: "10px",
  },
  smallMuted: {
    color: "#64748b",
    fontSize: "13px",
  },
  success: {
    background: "#ecfdf5",
    border: "1px solid #bbf7d0",
    color: "#166534",
    borderRadius: "18px",
    padding: "16px",
  },
  footerNote: {
    marginTop: "10px",
    color: "#475569",
    fontSize: "14px",
  },
};

function responsiveStyle(base, mobileOverrides) {
  if (typeof window !== "undefined" && window.innerWidth <= 860) {
    return { ...base, ...mobileOverrides };
  }
  return base;
}

export default function App() {
  const [profile, setProfile] = useState(() => loadFromStorage("english_app_profile", DEFAULT_PROFILE));
  const [progressData, setProgressData] = useState(() =>
    loadFromStorage("english_app_progress", {
      streak: 0,
      totalSessions: 0,
      totalScore: 0,
      lastSessionDate: null,
      lessonStats: {},
      notes: "",
      history: [],
    })
  );
  const [answers, setAnswers] = useState({});
  const [selfRating, setSelfRating] = useState({});
  const [sessionDone, setSessionDone] = useState(false);
  const [activeTab, setActiveTab] = useState("today");
  const [windowWidth, setWindowWidth] = useState(typeof window !== "undefined" ? window.innerWidth : 1200);

  useEffect(() => saveToStorage("english_app_profile", profile), [profile]);
  useEffect(() => saveToStorage("english_app_progress", progressData), [progressData]);

  useEffect(() => {
    function onResize() {
      setWindowWidth(window.innerWidth);
    }
    window.addEventListener("resize", onResize);
    return () => window.removeEventListener("resize", onResize);
  }, []);

  const dailyLessons = useMemo(() => getAdaptiveLessons(profile, progressData), [profile, progressData]);

  const averageScore = progressData.totalSessions
    ? Math.round(progressData.totalScore / progressData.totalSessions)
    : 0;

  const plannedToday = dailyLessons.length;
  const completedToday = Object.keys(selfRating).length;
  const progressPercent = plannedToday ? Math.round((completedToday / plannedToday) * 100) : 0;
  const isMobile = windowWidth <= 860;

  function updateProfile(field, value) {
    setProfile((prev) => ({ ...prev, [field]: value }));
  }

  function updateAnswer(id, value) {
    setAnswers((prev) => ({ ...prev, [id]: value }));
  }

  function updateRating(id, value) {
    setSelfRating((prev) => ({ ...prev, [id]: Number(value) }));
  }

  function finalizeSession() {
    if (!dailyLessons.length) return;
    const ratedLessons = dailyLessons.filter((l) => selfRating[l.id]);
    if (!ratedLessons.length) return;

    const today = todayKey();
    const sessionScore = Math.round(
      ratedLessons.reduce((acc, lesson) => acc + selfRating[lesson.id], 0) / ratedLessons.length
    );

    setProgressData((prev) => {
      const alreadyDoneToday = prev.lastSessionDate === today;
      const nextLessonStats = { ...prev.lessonStats };

      ratedLessons.forEach((lesson) => {
        const old = nextLessonStats[lesson.id] || { mastery: 0, reviews: 0, lastSeen: null };
        const responseLength = (answers[lesson.id] || "").trim().length;
        const answerBonus = responseLength >= 20 ? 10 : responseLength >= 8 ? 5 : 0;
        const newMastery = Math.min(100, Math.round(old.mastery * 0.6 + selfRating[lesson.id] * 0.3 + answerBonus));

        nextLessonStats[lesson.id] = {
          mastery: newMastery,
          reviews: old.reviews + 1,
          lastSeen: today,
          lastAnswer: answers[lesson.id] || "",
        };
      });

      const prevDate = prev.lastSessionDate ? new Date(prev.lastSessionDate) : null;
      const nowDate = new Date(today);
      let nextStreak = prev.streak;

      if (!alreadyDoneToday) {
        if (!prevDate) {
          nextStreak = 1;
        } else {
          const diff = Math.round((nowDate - prevDate) / (1000 * 60 * 60 * 24));
          if (diff === 1) nextStreak += 1;
          else if (diff > 1) nextStreak = 1;
        }
      }

      const nextHistory = [
        {
          date: today,
          score: sessionScore,
          lessons: ratedLessons.length,
        },
        ...prev.history,
      ].slice(0, 14);

      return {
        ...prev,
        streak: nextStreak,
        totalSessions: alreadyDoneToday ? prev.totalSessions : prev.totalSessions + 1,
        totalScore: alreadyDoneToday ? prev.totalScore : prev.totalScore + sessionScore,
        lastSessionDate: today,
        lessonStats: nextLessonStats,
        history: nextHistory,
      };
    });

    setSessionDone(true);
    setActiveTab("progress");
  }

  function resetAll() {
    localStorage.removeItem("english_app_profile");
    localStorage.removeItem("english_app_progress");
    setProfile(DEFAULT_PROFILE);
    setProgressData({
      streak: 0,
      totalSessions: 0,
      totalScore: 0,
      lastSessionDate: null,
      lessonStats: {},
      notes: "",
      history: [],
    });
    setAnswers({});
    setSelfRating({});
    setSessionDone(false);
    setActiveTab("today");
  }

  function saveNotes(value) {
    setProgressData((prev) => ({ ...prev, notes: value }));
  }

  const recommendation = useMemo(() => {
    if (averageScore >= 85)
      return "Você está pronto para usar frases mais longas e situações de trabalho mais complexas.";
    if (averageScore >= 65)
      return "Seu foco agora deve ser ganhar velocidade de resposta e repetir frases úteis diariamente.";
    if (averageScore >= 40)
      return "Você está no ponto ideal para repetir estruturas simples e falar sem traduzir palavra por palavra.";
    return "Seu melhor caminho é treinar frases curtas todos os dias, com calma e sem buscar perfeição.";
  }, [averageScore]);

  const heroGridStyle = responsiveStyle(styles.heroGrid, {
    gridTemplateColumns: "1fr",
  });

  const statsGridStyle = responsiveStyle(styles.statsGrid, {
    gridTemplateColumns: "1fr 1fr",
  });

  const lessonGridStyle = responsiveStyle(styles.lessonGrid, {
    gridTemplateColumns: "1fr",
  });

  const twoColsStyle = responsiveStyle(styles.twoCols, {
    gridTemplateColumns: "1fr",
  });

  return (
    <div style={styles.page}>
      <div style={styles.container}>
        <div style={heroGridStyle}>
          <section style={styles.card}>
            <div style={{ display: "flex", justifyContent: "space-between", gap: 12, flexWrap: "wrap" }}>
              <div>
                <h1 style={styles.title}>English Daily Coach</h1>
                <p style={styles.subtitle}>
                  Treino diário personalizado para quem tem pouco tempo e quer aprender a se comunicar com confiança.
                </p>
              </div>
              <span style={styles.badge}>Hoje: {todayKey()}</span>
            </div>

            <div style={statsGridStyle}>
              <div style={styles.statBox}>
                <div style={styles.label}>🔥 Sequência</div>
                <div style={styles.statValue}>{progressData.streak}</div>
                <div style={styles.statHelp}>dias seguidos</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.label}>🎯 Sessões</div>
                <div style={styles.statValue}>{progressData.totalSessions}</div>
                <div style={styles.statHelp}>realizadas</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.label}>🧠 Média</div>
                <div style={styles.statValue}>{averageScore}%</div>
                <div style={styles.statHelp}>{scoreLabel(averageScore)}</div>
              </div>
              <div style={styles.statBox}>
                <div style={styles.label}>⏱ Plano</div>
                <div style={styles.statValue}>{profile.dailyMinutes} min</div>
                <div style={styles.statHelp}>por dia</div>
              </div>
            </div>
          </section>

          <aside style={styles.card}>
            <h2 style={{ marginTop: 0, marginBottom: 6 }}>Seu foco atual</h2>
            <p style={{ ...styles.smallMuted, marginTop: 0, marginBottom: 18 }}>
              Personalize para o app adaptar o conteúdo.
            </p>

            <div style={styles.field}>
              <label style={styles.fieldLabel}>Nome</label>
              <input
                style={styles.input}
                value={profile.name}
                onChange={(e) => updateProfile("name", e.target.value)}
                placeholder="Seu nome"
              />
            </div>

            <div style={styles.field}>
              <label style={styles.fieldLabel}>Objetivo principal</label>
              <select
                style={styles.input}
                value={profile.focus}
                onChange={(e) => updateProfile("focus", e.target.value)}
              >
                <option value="work">Trabalho</option>
                <option value="conversation">Conversação</option>
                <option value="travel">Viagem</option>
              </select>
            </div>

            <div style={styles.field}>
              <label style={styles.fieldLabel}>Tempo diário</label>
              <select
                style={styles.input}
                value={profile.dailyMinutes}
                onChange={(e) => updateProfile("dailyMinutes", Number(e.target.value))}
              >
                <option value={10}>10 minutos</option>
                <option value={15}>15 minutos</option>
                <option value={20}>20 minutos</option>
                <option value={30}>30 minutos</option>
              </select>
            </div>
          </aside>
        </div>

        <div style={styles.tabs}>
          {[
            ["today", "Treino de hoje"],
            ["progress", "Progresso"],
            ["notes", "Anotações"],
          ].map(([key, label]) => (
            <button
              key={key}
              onClick={() => setActiveTab(key)}
              style={{
                ...styles.tabButton,
                ...(activeTab === key ? styles.activeTabButton : {}),
              }}
            >
              {label}
            </button>
          ))}
        </div>

        {activeTab === "today" && (
          <div>
            <section style={{ ...styles.card, marginBottom: 16 }}>
              <div
                style={{
                  display: "flex",
                  justifyContent: "space-between",
                  gap: 16,
                  alignItems: isMobile ? "stretch" : "center",
                  flexDirection: isMobile ? "column" : "row",
                }}
              >
                <div>
                  <h2 style={{ margin: 0, marginBottom: 6 }}>Plano de hoje para {profile.name}</h2>
                  <p style={{ ...styles.smallMuted, margin: 0 }}>
                    O conteúdo abaixo é montado com base no seu foco, tempo disponível e desempenho anterior.
                  </p>
                </div>
                <div style={{ minWidth: isMobile ? "100%" : 240 }}>
                  <div style={{ ...styles.smallMuted, marginBottom: 8 }}>Conclusão do dia</div>
                  <div style={styles.progressWrap}>
                    <div style={{ ...styles.progressBar, width: `${progressPercent}%` }} />
                  </div>
                  <div style={{ ...styles.smallMuted, marginTop: 8 }}>
                    {completedToday}/{plannedToday} atividades avaliadas
                  </div>
                </div>
              </div>
            </section>

            <div style={styles.lessonsList}>
              {dailyLessons.map((lesson) => (
                <section key={lesson.id} style={styles.card}>
                  <div style={styles.pillRow}>
                    <span style={styles.pill}>{lesson.theme}</span>
                    <span style={styles.pill}>Nível {lesson.difficulty}</span>
                    <span style={styles.pill}>{lesson.category}</span>
                  </div>

                  <div style={lessonGridStyle}>
                    <div>
                      <div style={styles.label}>Frase principal</div>
                      <div style={styles.english}>{lesson.english}</div>

                      <div style={styles.box}>
                        <div style={styles.label}>Significado</div>
                        <div>{lesson.portuguese}</div>
                      </div>

                      <div style={styles.box}>
                        <div style={styles.label}>Situação real</div>
                        <div>{lesson.prompt}</div>
                      </div>

                      <div style={styles.box}>
                        <div style={styles.label}>Variações úteis</div>
                        <div style={styles.pillRow}>
                          {lesson.variations.map((variation) => (
                            <span key={variation} style={styles.pill}>
                              {variation}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    <div>
                      <div style={styles.box}>
                        <div style={{ fontWeight: 800, marginBottom: 8 }}>💬 Sua resposta</div>
                        <div style={{ ...styles.smallMuted, marginBottom: 10 }}>
                          Escreva do seu jeito. O objetivo é praticar, não buscar perfeição.
                        </div>
                        <textarea
                          style={styles.textarea}
                          value={answers[lesson.id] || ""}
                          onChange={(e) => updateAnswer(lesson.id, e.target.value)}
                          placeholder="Ex.: I work with IT and process improvement..."
                        />
                      </div>

                      <div style={styles.box}>
                        <div style={{ fontWeight: 800, marginBottom: 8 }}>🎙 Autoavaliação</div>
                        <div style={{ ...styles.smallMuted, marginBottom: 10 }}>
                          Dê uma nota para como você conseguiu falar ou escrever essa frase hoje.
                        </div>
                        <select
                          style={styles.input}
                          value={selfRating[lesson.id] || ""}
                          onChange={(e) => updateRating(lesson.id, e.target.value)}
                        >
                          <option value="">Escolha sua nota</option>
                          <option value="25">25% — muito difícil</option>
                          <option value="50">50% — consegui com ajuda</option>
                          <option value="75">75% — consegui razoavelmente</option>
                          <option value="100">100% — consegui bem</option>
                        </select>
                      </div>
                    </div>
                  </div>
                </section>
              ))}
            </div>

            <div style={styles.actionRow}>
              <button style={styles.button} onClick={finalizeSession}>
                ✅ Finalizar sessão de hoje
              </button>
              <button
                style={{ ...styles.button, ...styles.secondaryButton }}
                onClick={() => {
                  setAnswers({});
                  setSelfRating({});
                  setSessionDone(false);
                }}
              >
                🔄 Limpar respostas
              </button>
            </div>

            {sessionDone && (
              <div style={{ ...styles.card, marginTop: 16 }}>
                <div style={styles.success}>
                  <strong>Sessão salva com sucesso.</strong>
                  <div style={styles.footerNote}>
                    Amanhã o app vai priorizar conteúdos em que você teve mais dificuldade, além de manter seu foco principal.
                  </div>
                </div>
              </div>
            )}
          </div>
        )}

        {activeTab === "progress" && (
          <div style={twoColsStyle}>
            <section style={styles.card}>
              <h2 style={{ marginTop: 0 }}>Resumo do aprendizado</h2>
              <p style={{ ...styles.smallMuted, marginTop: 0 }}>Visão geral do seu ritmo e adaptação do conteúdo.</p>

              <div style={styles.box}>
                <div style={styles.label}>Diagnóstico atual</div>
                <div style={{ fontSize: 22, fontWeight: 800, marginBottom: 8 }}>{scoreLabel(averageScore)}</div>
                <div>{recommendation}</div>
              </div>

              <div style={styles.box}>
                <div style={styles.label}>Última sessão registrada</div>
                <div style={{ fontSize: 18, fontWeight: 800 }}>{progressData.lastSessionDate || "Nenhuma ainda"}</div>
              </div>
            </section>

            <section style={styles.card}>
              <h2 style={{ marginTop: 0 }}>Histórico recente</h2>
              <p style={{ ...styles.smallMuted, marginTop: 0 }}>Últimas 14 sessões registradas.</p>

              {progressData.history.length === 0 ? (
                <div style={styles.smallMuted}>Seu histórico aparecerá aqui após a primeira sessão.</div>
              ) : (
                progressData.history.map((item) => (
                  <div key={`${item.date}-${item.score}`} style={styles.historyItem}>
                    <div>
                      <div style={{ fontWeight: 800 }}>{item.date}</div>
                      <div style={styles.smallMuted}>{item.lessons} lições avaliadas</div>
                    </div>
                    <span style={styles.badge}>{item.score}%</span>
                  </div>
                ))
              )}

              <div style={{ marginTop: 18 }}>
                <button style={{ ...styles.button, ...styles.dangerButton }} onClick={resetAll}>
                  Reiniciar progresso
                </button>
              </div>
            </section>
          </div>
        )}

        {activeTab === "notes" && (
          <section style={styles.card}>
            <h2 style={{ marginTop: 0 }}>Anotações pessoais</h2>
            <p style={{ ...styles.smallMuted, marginTop: 0 }}>
              Registre erros frequentes, frases que quer memorizar ou situações reais que quer praticar.
            </p>
            <textarea
              style={{ ...styles.textarea, minHeight: 260 }}
              value={progressData.notes}
              onChange={(e) => saveNotes(e.target.value)}
              placeholder="Ex.: Tenho dificuldade em responder rápido em reuniões. Quero praticar apresentação pessoal e frases de alinhamento..."
            />
          </section>
        )}
      </div>
    </div>
  );
}
