// TypeScript Definitions for Simple AI Interview Coach

export interface UserProfile {
  user_id: number;
  name: str;
  education?: string;
  experience_level?: string;
  target_role: string;
  target_company?: string;
}

export interface DocumentInfo {
  document_id: number;
  filename: string;
  doc_type: string;
  extracted_text_preview: string;
}

export interface AssessmentQuestion {
  question_id: number;
  question_text: string;
  topic: string;
  difficulty: string;
  options?: string[];
  step: number;
  total_steps: number;
}

export interface DashboardData {
  user_name: string;
  target_role: string;
  preparation_percentage: number;
  todays_focus: string;
  motivational_quote: string;
  daily_streak: number;
  recent_scores: number[];
  strong_topics: string[];
  weak_topics: string[];
}

export interface SocraticLearningSession {
  learning_session_id: number;
  topic: string;
  explanation: string;
  code_example?: string;
  question_id: number;
  question_text: string;
  difficulty: string;
}

export interface InterviewSession {
  interview_session_id: number;
  mode: 'HR' | 'Technical' | 'Resume/Project';
  question_id: number;
  question_text: string;
  current_index: number;
  total_questions: number;
}

export interface InterviewFeedbackReport {
  feedback_id: number;
  session_id: number;
  overall_score: number;
  technical_score: number;
  communication_score: number;
  confidence_score: number;
  what_did_well: string[];
  improve: string[];
  habits_to_reduce: string[];
  what_to_say: Array<{ instead_of: string; say: string }>;
  avoid: string[];
  next_focus: string[];
}

export interface ProgressSummary {
  overall_percentage: number;
  daily_streak: number;
  strong_topics: string[];
  weak_topics: string[];
  recent_scores: number[];
  recommended_next: string;
}
