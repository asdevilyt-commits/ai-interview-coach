// Global Client State
let userId = 1;
let currentAssessmentId = null;
let currentAssessmentQuestionId = null;
let currentAssessmentStep = 1;
let currentLearningSessionId = null;
let currentLearningQuestionId = null;
let currentInterviewSessionId = null;
let currentInterviewQuestionId = null;
let currentInterviewMode = 'Technical';
let selectedAssessmentChoice = null;
let speechRecognition = null;
let isRecordingVoice = false;

// Base API URL
const API_BASE = "";

// Initialize App
document.addEventListener("DOMContentLoaded", () => {
  autoRegisterUser();
  loadDashboard();
  loadProgress();
  setupVoiceRecognition();
});

// Auto Register or Fetch Default User
async function autoRegisterUser() {
  try {
    const res = await fetch(`${API_BASE}/register`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username: "alex_student" })
    });
    if (res.ok) {
      const data = await res.json();
      userId = data.user_id;
    }
  } catch (err) {
    console.warn("Using default user_id = 1", err);
  }
}

// Tab Navigation Manager
function switchTab(tabName) {
  const tabs = document.querySelectorAll(".tab-pane");
  const navItems = document.querySelectorAll(".nav-item");

  tabs.forEach(tab => tab.classList.remove("active"));
  navItems.forEach(item => item.classList.remove("active"));

  const targetPane = document.getElementById(tabName);
  if (targetPane) targetPane.classList.add("active");

  const targetNav = document.querySelector(`.nav-item[data-tab="${tabName}"]`);
  if (targetNav) targetNav.classList.add("active");

  if (tabName === "home") loadDashboard();
  if (tabName === "progress") loadProgress();
}

// ==================== DASHBOARD ====================
async function loadDashboard() {
  try {
    const res = await fetch(`${API_BASE}/dashboard?user_id=${userId}`);
    if (res.ok) {
      const data = await res.json();
      document.getElementById("home-greeting").innerText = `Welcome back, ${data.user_name} 👋`;
      document.getElementById("home-quote").innerText = `"${data.motivational_quote}"`;
      document.getElementById("home-prep-badge").innerText = `${data.preparation_percentage}% Prepared`;
      document.getElementById("home-target-role").innerText = data.target_role;
      document.getElementById("home-focus-topic").innerText = data.todays_focus;
      document.getElementById("home-prep-pct").innerText = `${data.preparation_percentage}%`;
      document.getElementById("home-prep-fill").style.width = `${data.preparation_percentage}%`;
      document.getElementById("header-streak-pill").innerText = `🔥 ${data.daily_streak}-Day Streak`;

      // Render Strong Topics
      const strongContainer = document.getElementById("home-strong-list");
      strongContainer.innerHTML = data.strong_topics.map(t => `<span class="badge badge-success">✓ ${t}</span>`).join('');

      // Render Weak Topics
      const weakContainer = document.getElementById("home-weak-list");
      weakContainer.innerHTML = data.weak_topics.map(t => `<span class="badge badge-warning">⚠ ${t}</span>`).join('');
    }
  } catch (err) {
    console.error("Dashboard error:", err);
  }
}

// ==================== ONBOARDING FLOW (8 STEPS) ====================
function openOnboardingModal() {
  document.getElementById("onboarding-modal").style.display = "flex";
  nextOnboardingStep(1);
}

function closeOnboardingModal() {
  document.getElementById("onboarding-modal").style.display = "none";
  loadDashboard();
}

function nextOnboardingStep(stepNum) {
  const steps = document.querySelectorAll(".ob-step");
  steps.forEach(s => s.style.display = "none");

  const targetStep = document.getElementById(`ob-step-${stepNum}`);
  if (targetStep) targetStep.style.display = "block";

  document.getElementById("ob-step-badge").innerText = `Step ${stepNum} of 8`;
}

async function uploadObResumeAndNext() {
  const fileInput = document.getElementById("ob-resume-file");
  if (fileInput.files.length > 0) {
    const formData = new FormData();
    formData.append("user_id", userId);
    formData.append("doc_type", "resume");
    formData.append("file", fileInput.files[0]);

    try {
      await fetch(`${API_BASE}/documents/upload`, { method: "POST", body: formData });
    } catch (e) {
      console.warn("Resume upload non-blocking error", e);
    }
  }
  nextOnboardingStep(4);
}

async function saveObProfileAndStartAssessment() {
  const name = document.getElementById("ob-name").value || "Alex";
  const edu = document.getElementById("ob-edu").value || "Computer Science";
  const exp = document.getElementById("ob-exp").value || "Entry Level";
  const role = document.getElementById("ob-target-role").value || "AI Engineer";
  const comp = document.getElementById("ob-target-company").value || "";

  try {
    await fetch(`${API_BASE}/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        name: name,
        education: edu,
        experience_level: exp,
        target_role: role,
        target_company: comp
      })
    });
  } catch (e) {
    console.error("Profile save error", e);
  }

  // Start Assessment
  nextOnboardingStep(6);
  startAssessment();
}

async function startAssessment() {
  try {
    const res = await fetch(`${API_BASE}/assessment/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId })
    });
    if (res.ok) {
      const data = await res.json();
      currentAssessmentId = data.assessment_id;
      currentAssessmentQuestionId = data.question_id;
      currentAssessmentStep = data.step;
      renderAssessmentQuestion(data);
    }
  } catch (err) {
    console.error("Start assessment error:", err);
  }
}

function renderAssessmentQuestion(data) {
  document.getElementById("ob-assess-topic").innerText = `Assessment: ${data.topic} (${data.difficulty})`;
  document.getElementById("ob-assess-step-counter").innerText = `Q ${data.step} of ${data.total_steps}`;
  document.getElementById("ob-assess-q-text").innerText = data.question_text;

  const container = document.getElementById("ob-assess-options-container");
  container.innerHTML = "";
  selectedAssessmentChoice = null;

  if (data.options && data.options.length > 0) {
    data.options.forEach((opt) => {
      const btn = document.createElement("button");
      btn.className = "btn btn-secondary";
      btn.style.textAlign = "left";
      btn.innerText = opt;
      btn.onclick = () => {
        const siblings = container.querySelectorAll("button");
        siblings.forEach(b => b.className = "btn btn-secondary");
        btn.className = "btn btn-primary";
        selectedAssessmentChoice = opt;
      };
      container.appendChild(btn);
    });
  } else {
    const input = document.createElement("input");
    input.type = "text";
    input.className = "input-box";
    input.placeholder = "Type your answer...";
    input.oninput = (e) => { selectedAssessmentChoice = e.target.value; };
    container.appendChild(input);
  }
}

async function submitAssessmentAnswer() {
  if (!selectedAssessmentChoice) {
    alert("Please select or type an answer before proceeding.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/assessment/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        assessment_id: currentAssessmentId,
        question_id: currentAssessmentQuestionId,
        user_answer: selectedAssessmentChoice
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (data.is_completed) {
        // Render Personalised Plan
        const summary = data.result_summary;
        if (summary && summary.personalized_plan) {
          const plan = summary.personalized_plan;
          document.getElementById("ob-plan-phase1").innerText = `Phase 1: ${plan.phase_1}`;
          document.getElementById("ob-plan-phase2").innerText = `Phase 2: ${plan.phase_2}`;
          document.getElementById("ob-plan-phase3").innerText = `Phase 3: ${plan.phase_3}`;
        }
        nextOnboardingStep(7);
      } else if (data.next_question) {
        currentAssessmentQuestionId = data.next_question.question_id;
        currentAssessmentStep = data.next_question.step;
        renderAssessmentQuestion(data.next_question);
      }
    }
  } catch (err) {
    console.error("Submit assessment answer error:", err);
  }
}

// ==================== SOCRATIC LEARNING ====================
async function loadRecommendedTopic() {
  try {
    const res = await fetch(`${API_BASE}/progress?user_id=${userId}`);
    if (res.ok) {
      const data = await res.json();
      const topic = data.recommended_next || "SQL Joins";
      document.getElementById("learn-topic-input").value = topic;
      startLearningTopic(topic);
    }
  } catch (err) {
    startLearningTopic("SQL Joins");
  }
}

async function startLearningTopic(customTopic) {
  const topic = customTopic || document.getElementById("learn-topic-input").value || "SQL Joins";
  try {
    const res = await fetch(`${API_BASE}/learning/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, topic: topic })
    });

    if (res.ok) {
      const data = await res.json();
      currentLearningSessionId = data.learning_session_id;
      currentLearningQuestionId = data.question_id;

      document.getElementById("learn-topic-title").innerText = `${data.topic} — Socratic Guidance`;
      document.getElementById("learn-explanation-body").innerHTML = marked.parse(data.explanation || "");

      const codeContainer = document.getElementById("learn-code-container");
      if (data.code_example) {
        codeContainer.style.display = "block";
        document.getElementById("learn-code-body").innerHTML = marked.parse(data.code_example);
      } else {
        codeContainer.style.display = "none";
      }

      document.getElementById("learn-question-text").innerText = data.question_text;
      document.getElementById("learn-answer-input").value = "";
      document.getElementById("learn-eval-output").style.display = "none";
    }
  } catch (err) {
    console.error("Start learning error:", err);
  }
}

async function submitLearningAnswer() {
  const answer = document.getElementById("learn-answer-input").value;
  if (!answer.trim()) {
    alert("Please enter your answer.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/learning/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        learning_session_id: currentLearningSessionId,
        question_id: currentLearningQuestionId,
        user_answer: answer
      })
    });

    if (res.ok) {
      const data = await res.json();
      document.getElementById("learn-eval-output").style.display = "block";
      document.getElementById("learn-eval-text").innerHTML = marked.parse(data.ai_feedback);
    }
  } catch (err) {
    console.error("Submit learning answer error:", err);
  }
}

// ==================== MOCK INTERVIEW ====================
function selectInterviewMode(mode) {
  currentInterviewMode = mode;
  ['HR', 'Technical', 'Resume/Project'].forEach(m => {
    const card = document.getElementById(`mode-card-${m}`);
    if (card) card.style.border = (m === mode) ? "2px solid var(--accent-primary)" : "1px solid var(--border-color)";
  });

  startMockInterview();
}

async function startMockInterview() {
  try {
    const res = await fetch(`${API_BASE}/interview/start`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, mode: currentInterviewMode })
    });

    if (res.ok) {
      const data = await res.json();
      currentInterviewSessionId = data.interview_session_id;
      currentInterviewQuestionId = data.question_id;

      document.getElementById("interview-active-area").style.display = "block";
      document.getElementById("interview-report-area").style.display = "none";
      document.getElementById("interview-mode-badge").innerText = `${data.mode} Interview`;
      document.getElementById("interview-step-counter").innerText = `Question ${data.current_index + 1} of ${data.total_questions}`;
      document.getElementById("interview-question-text").innerText = data.question_text;
      document.getElementById("interview-answer-input").value = "";
      document.getElementById("interview-eval-box").style.display = "none";
    }
  } catch (err) {
    console.error("Start interview error:", err);
  }
}

async function submitInterviewAnswer() {
  const ans = document.getElementById("interview-answer-input").value;
  if (!ans.trim()) {
    alert("Please provide an answer either by typing or using voice.");
    return;
  }

  try {
    const res = await fetch(`${API_BASE}/interview/answer`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        interview_session_id: currentInterviewSessionId,
        question_id: currentInterviewQuestionId,
        user_answer: ans
      })
    });

    if (res.ok) {
      const data = await res.json();
      if (data.is_completed && data.feedback_id) {
        loadInterviewFeedbackReport(data.feedback_id);
      } else if (data.next_question) {
        currentInterviewQuestionId = data.next_question.question_id;
        document.getElementById("interview-step-counter").innerText = `Question ${data.next_question.current_index + 1} of ${data.next_question.total_questions}`;
        document.getElementById("interview-question-text").innerText = data.next_question.question_text;
        document.getElementById("interview-answer-input").value = "";

        if (data.ai_evaluation) {
          document.getElementById("interview-eval-box").style.display = "block";
          document.getElementById("interview-eval-text").innerHTML = marked.parse(data.ai_evaluation);
        }
      }
    }
  } catch (err) {
    console.error("Submit interview answer error:", err);
  }
}

async function loadInterviewFeedbackReport(feedbackId) {
  try {
    const res = await fetch(`${API_BASE}/interview/${feedbackId}/feedback`);
    if (res.ok) {
      const data = await res.json();
      document.getElementById("interview-active-area").style.display = "none";
      document.getElementById("interview-report-area").style.display = "block";

      document.getElementById("report-overall-score").innerText = `${data.overall_score}%`;
      document.getElementById("report-tech-score").innerText = `${data.technical_score}%`;
      document.getElementById("report-comm-score").innerText = `${data.communication_score}%`;

      document.getElementById("report-well-list").innerHTML = data.what_did_well.map(item => `<li>✓ ${item}</li>`).join('');
      document.getElementById("report-improve-list").innerHTML = data.improve.map(item => `<li>• ${item}</li>`).join('');
      document.getElementById("report-habits-list").innerHTML = data.habits_to_reduce.map(item => `<li>⚠️ ${item}</li>`).join('');
      
      const sayBox = document.getElementById("report-say-container");
      sayBox.innerHTML = data.what_to_say.map(item => `
        <div class="compare-box">
          <div class="instead-text">Instead of: "${item.instead_of}"</div>
          <div class="say-text">Say: "${item.say}"</div>
        </div>
      `).join('');

      document.getElementById("report-avoid-list").innerHTML = data.avoid.map(item => `<li>🚫 ${item}</li>`).join('');
      document.getElementById("report-focus-list").innerHTML = data.next_focus.map(item => `<li>🎯 ${item}</li>`).join('');
    }
  } catch (err) {
    console.error("Feedback report error:", err);
  }
}

function resetInterviewSession() {
  document.getElementById("interview-report-area").style.display = "none";
  document.getElementById("interview-active-area").style.display = "none";
}

// ==================== VOICE INTERVIEW (WEB SPEECH API) ====================
function setupVoiceRecognition() {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (SpeechRecognition) {
    speechRecognition = new SpeechRecognition();
    speechRecognition.continuous = true;
    speechRecognition.interimResults = true;
    speechRecognition.lang = 'en-US';

    speechRecognition.onresult = (event) => {
      let transcript = '';
      for (let i = event.resultIndex; i < event.results.length; i++) {
        transcript += event.results[i][0].transcript;
      }
      document.getElementById("interview-answer-input").value = transcript;
    };

    speechRecognition.onerror = (event) => {
      console.warn("Speech recognition error", event.error);
      stopVoiceRecording();
    };

    speechRecognition.onend = () => {
      if (isRecordingVoice) {
        stopVoiceRecording();
      }
    };
  }
}

function toggleVoiceRecognition() {
  if (!speechRecognition) {
    alert("Speech recognition is not supported in this browser. Please type your answer.");
    return;
  }

  if (isRecordingVoice) {
    stopVoiceRecording();
  } else {
    startVoiceRecording();
  }
}

function startVoiceRecording() {
  try {
    speechRecognition.start();
    isRecordingVoice = true;
    const btn = document.getElementById("btn-start-voice");
    btn.className = "btn btn-primary mic-pulse";
    btn.innerText = "🛑 Stop Recording";
    document.getElementById("voice-status-text").innerText = "Listening... Speak your answer clearly.";
  } catch (e) {
    console.error("Voice start error", e);
  }
}

function stopVoiceRecording() {
  try {
    speechRecognition.stop();
  } catch (e) {}
  isRecordingVoice = false;
  const btn = document.getElementById("btn-start-voice");
  btn.className = "btn btn-outline";
  btn.innerText = "🎤 Start Voice Interview";
  document.getElementById("voice-status-text").innerText = "Voice captured. You can edit the text before submitting.";
}

// ==================== PROGRESS ====================
async function loadProgress() {
  try {
    const res = await fetch(`${API_BASE}/progress?user_id=${userId}`);
    if (res.ok) {
      const data = await res.json();
      document.getElementById("prog-overall-pct").innerText = `${data.overall_percentage}%`;
      document.getElementById("prog-overall-fill").style.width = `${data.overall_percentage}%`;
      document.getElementById("prog-rec-next").innerText = data.recommended_next;

      document.getElementById("prog-strong-container").innerHTML = data.strong_topics.map(t => `<div class="badge badge-success" style="font-size: 0.9rem; padding: 8px 14px;">✓ ${t}</div>`).join('');
      document.getElementById("prog-weak-container").innerHTML = data.weak_topics.map(t => `<div class="badge badge-warning" style="font-size: 0.9rem; padding: 8px 14px;">⚠️ ${t}</div>`).join('');
    }
  } catch (err) {
    console.error("Progress load error:", err);
  }
}

// ==================== PROFILE & DOCUMENT MANAGEMENT ====================
async function saveProfileChanges() {
  const name = document.getElementById("prof-name-input").value;
  const edu = document.getElementById("prof-edu-input").value;
  const exp = document.getElementById("prof-exp-input").value;
  const role = document.getElementById("prof-role-input").value;
  const comp = document.getElementById("prof-company-input").value;

  try {
    const res = await fetch(`${API_BASE}/profile`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        user_id: userId,
        name: name,
        education: edu,
        experience_level: exp,
        target_role: role,
        target_company: comp
      })
    });
    if (res.ok) {
      alert("Profile updated successfully!");
      loadDashboard();
    }
  } catch (err) {
    console.error("Profile save error:", err);
  }
}

async function uploadDocumentFile() {
  const docType = document.getElementById("doc-type-select").value;
  const fileInput = document.getElementById("doc-file-input");

  if (fileInput.files.length === 0) {
    alert("Please select a file to upload.");
    return;
  }

  const formData = new FormData();
  formData.append("user_id", userId);
  formData.append("doc_type", docType);
  formData.append("file", fileInput.files[0]);

  try {
    const res = await fetch(`${API_BASE}/documents/upload`, {
      method: "POST",
      body: formData
    });

    if (res.ok) {
      const data = await res.json();
      alert(`Document '${data.filename}' uploaded and indexed into FAISS RAG store!`);
      const container = document.getElementById("doc-list-container");
      container.innerHTML += `
        <div style="background: #ffffff; border: 1px solid var(--border-color); padding: 12px; border-radius: var(--radius-sm); margin-top: 8px;">
          <strong>${data.filename}</strong> (${data.doc_type})
          <div style="font-size: 0.8rem; color: var(--text-muted); margin-top: 4px;">${data.extracted_text_preview}</div>
        </div>
      `;
      fileInput.value = "";
    }
  } catch (err) {
    console.error("Document upload error:", err);
  }
}
