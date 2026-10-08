import { useEffect, useState } from "react";
import {
  createConstraint,
  createDietPlan,
  createHealthMetric,
  createProfile,
  getConstraints,
  getCurrentUser,
  getDietPlans,
  getHealthMetrics,
  getProfile,
  loginUser,
  logoutUser,
  registerUser,
  updateProfile,
  updateUser,
} from "./services/api";

const initialProfileForm = {
  nickname: "",
  profile_image_url: "",
  introduction: "",
};

const initialRegisterForm = {
  login_id: "",
  name: "",
  email: "",
  password: "",
  phone_number: "",
  gender: "M",
};

const initialLoginForm = {
  login_id: "",
  password: "",
};

function App() {
  const [profileForm, setProfileForm] = useState(initialProfileForm);
  const [profileLoading, setProfileLoading] = useState(true);
  const [profileMessage, setProfileMessage] = useState("");
  const [isNewProfile, setIsNewProfile] = useState(false);

  const [currentUser, setCurrentUser] = useState(null);
  const [userForm, setUserForm] = useState(initialRegisterForm);
  const [userMessage, setUserMessage] = useState("");
  const [loginForm, setLoginForm] = useState(initialLoginForm);
  const [loginMessage, setLoginMessage] = useState("");
  const [authMode, setAuthMode] = useState("login");
  const [healthForm, setHealthForm] = useState({ height: "", weight: "" });
  const [healthMetrics, setHealthMetrics] = useState([]);
  const [healthMessage, setHealthMessage] = useState("");
  const [constraintForm, setConstraintForm] = useState({ constraint_type: "", constraint_value: "" });
  const [constraints, setConstraints] = useState([]);
  const [constraintMessage, setConstraintMessage] = useState("");
  const [dietPlanForm, setDietPlanForm] = useState({ breakfast: "", lunch: "", dinner: "" });
  const [dietPlans, setDietPlans] = useState([]);
  const [dietPlanMessage, setDietPlanMessage] = useState("");

  useEffect(() => {
    const savedUserId = localStorage.getItem("userId");
    if (savedUserId) {
      loadCurrentUser();
    }
  }, []);

  const loadCurrentUser = async () => {
    try {
      const user = await getCurrentUser();
      setCurrentUser(user);
      setUserForm({
        login_id: user.login_id,
        name: user.name,
        email: user.email,
        password: "",
        phone_number: user.phone_number || "",
        gender: user.gender || "M",
      });
      await loadProfile();
      await loadHealthMetrics();
      await loadConstraints();
      await loadDietPlans();
    } catch (error) {
      setCurrentUser(null);
      logoutUser();
    }
  };

  const loadHealthMetrics = async () => {
    try {
      const metrics = await getHealthMetrics();
      setHealthMetrics(metrics);
    } catch (error) {
      setHealthMetrics([]);
    }
  };

  const loadConstraints = async () => {
    try {
      const items = await getConstraints();
      setConstraints(items);
    } catch (error) {
      setConstraints([]);
    }
  };

  const loadDietPlans = async () => {
    try {
      const plans = await getDietPlans();
      setDietPlans(plans);
    } catch (error) {
      setDietPlans([]);
    }
  };

  const loadProfile = async () => {
    try {
      setProfileLoading(true);
      const profile = await getProfile();
      setProfileForm({
        nickname: profile.nickname || "",
        profile_image_url: profile.profile_image_url || "",
        introduction: profile.introduction || "",
      });
      setIsNewProfile(false);
      setProfileMessage("프로필을 불러왔습니다.");
    } catch (error) {
      if (error.response?.status === 404) {
        setIsNewProfile(true);
        setProfileMessage("프로필이 아직 없습니다. 새로 등록해 주세요.");
      } else {
        setProfileMessage("프로필을 불러오지 못했습니다.");
      }
    } finally {
      setProfileLoading(false);
    }
  };

  const handleProfileChange = (event) => {
    const { name, value } = event.target;
    setProfileForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleUserChange = (event) => {
    const { name, value } = event.target;
    setUserForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleHealthChange = (event) => {
    const { name, value } = event.target;
    setHealthForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleConstraintChange = (event) => {
    const { name, value } = event.target;
    setConstraintForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleDietPlanChange = (event) => {
    const { name, value } = event.target;
    setDietPlanForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleLoginChange = (event) => {
    const { name, value } = event.target;
    setLoginForm((prev) => ({
      ...prev,
      [name]: value,
    }));
  };

  const handleLoginSubmit = async (event) => {
    event.preventDefault();
    try {
      setLoginMessage("");
      const user = await loginUser(loginForm);
      setCurrentUser(user);
      setUserForm({
        login_id: user.login_id,
        name: user.name,
        email: user.email,
        password: "",
        phone_number: user.phone_number || "",
        gender: user.gender || "M",
      });
      setAuthMode("login");
      await loadProfile();
      await loadHealthMetrics();
      await loadConstraints();
      await loadDietPlans();
      setLoginMessage("로그인 되었습니다.");
    } catch (error) {
      setLoginMessage(error.response?.data?.detail || "로그인에 실패했습니다.");
    }
  };

  const handleHealthSubmit = async (event) => {
    event.preventDefault();
    try {
      setHealthMessage("");
      const payload = {
        height: Number(healthForm.height),
        weight: Number(healthForm.weight),
      };
      const saved = await createHealthMetric(payload);
      setHealthMetrics((prev) => [saved, ...prev]);
      setHealthForm({ height: "", weight: "" });
      setHealthMessage("건강 지표가 저장되었습니다.");
    } catch (error) {
      setHealthMessage(error.response?.data?.detail || "건강 지표 저장 중 오류가 발생했습니다.");
    }
  };

  const handleConstraintSubmit = async (event) => {
    event.preventDefault();
    try {
      setConstraintMessage("");
      const saved = await createConstraint(constraintForm);
      setConstraints((prev) => [saved, ...prev]);
      setConstraintForm({ constraint_type: "", constraint_value: "" });
      setConstraintMessage("제약 조건이 저장되었습니다.");
    } catch (error) {
      setConstraintMessage(error.response?.data?.detail || "제약 조건 저장 중 오류가 발생했습니다.");
    }
  };

  const handleDietPlanSubmit = async (event) => {
    event.preventDefault();
    try {
      setDietPlanMessage("");
      const payload = { plan_details: { ...dietPlanForm } };
      const saved = await createDietPlan(payload);
      setDietPlans((prev) => [saved, ...prev]);
      setDietPlanForm({ breakfast: "", lunch: "", dinner: "" });
      setDietPlanMessage("식단 플랜이 저장되었습니다.");
    } catch (error) {
      setDietPlanMessage(error.response?.data?.detail || "식단 플랜 저장 중 오류가 발생했습니다.");
    }
  };

  const handleRegisterSubmit = async (event) => {
    event.preventDefault();
    try {
      setUserMessage("");
      const created = await registerUser(userForm);
      setCurrentUser(created);
      setUserForm({
        login_id: created.login_id,
        name: created.name,
        email: created.email,
        password: "",
        phone_number: created.phone_number || "",
        gender: created.gender || "M",
      });
      setAuthMode("login");
      await loadProfile();
      setUserMessage("회원가입이 완료되었습니다.");
    } catch (error) {
      setUserMessage(error.response?.data?.detail || "회원가입에 실패했습니다.");
    }
  };

  const handleProfileSubmit = async (event) => {
    event.preventDefault();

    try {
      setProfileMessage("");
      if (isNewProfile) {
        await createProfile(profileForm);
        setProfileMessage("프로필이 생성되었습니다.");
      } else {
        await updateProfile(profileForm);
        setProfileMessage("프로필이 수정되었습니다.");
      }
      setIsNewProfile(false);
      await loadProfile();
    } catch (error) {
      setProfileMessage(error.response?.data?.detail || "저장 중 오류가 발생했습니다.");
    }
  };

  const handleUserUpdate = async (event) => {
    event.preventDefault();

    try {
      setUserMessage("");
      const payload = {
        name: userForm.name,
        email: userForm.email,
        phone_number: userForm.phone_number,
        gender: userForm.gender,
      };

      const updated = await updateUser(payload);
      setCurrentUser(updated);
      setUserMessage("회원 정보가 수정되었습니다.");
    } catch (error) {
      setUserMessage(error.response?.data?.detail || "회원 수정 중 오류가 발생했습니다.");
    }
  };

  const handleLogout = () => {
    logoutUser();
    setCurrentUser(null);
    setProfileForm(initialProfileForm);
    setProfileMessage("");
    setUserForm(initialRegisterForm);
    setLoginForm(initialLoginForm);
    setHealthForm({ height: "", weight: "" });
    setHealthMetrics([]);
    setConstraintForm({ constraint_type: "", constraint_value: "" });
    setConstraints([]);
      setDietPlanForm({ breakfast: "", lunch: "", dinner: "" });
      setDietPlans([]);
    return (
      <div className="page-shell auth-page">
        <div className="auth-card">
          <div className="auth-header">
            <p className="eyebrow">Wellness</p>
            <h1>Welcome</h1>
          </div>

          <div className="auth-toggle">
            <button
              type="button"
              className={authMode === "login" ? "active" : ""}
              onClick={() => setAuthMode("login")}
            >
              로그인
            </button>
            <button
              type="button"
              className={authMode === "register" ? "active" : ""}
              onClick={() => setAuthMode("register")}
            >
              회원가입
            </button>
          </div>

          {authMode === "login" ? (
            <form onSubmit={handleLoginSubmit} className="profile-form">
              <label>
                로그인 ID
                <input
                  name="login_id"
                  value={loginForm.login_id}
                  onChange={handleLoginChange}
                  placeholder="login_id"
                />
              </label>

              <label>
                비밀번호
                <input
                  type="password"
                  name="password"
                  value={loginForm.password}
                  onChange={handleLoginChange}
                  placeholder="비밀번호 입력"
                />
              </label>

              <button type="submit">로그인</button>
              {loginMessage && <p className="status-message">{loginMessage}</p>}
            </form>
          ) : (
            <form onSubmit={handleRegisterSubmit} className="profile-form">
              <label>
                로그인 ID
                <input
                  name="login_id"
                  value={userForm.login_id}
                  onChange={handleUserChange}
                  placeholder="login_id"
                />
              </label>

              <label>
                비밀번호
                <input
                  type="password"
                  name="password"
                  value={userForm.password}
                  onChange={handleUserChange}
                  placeholder="비밀번호 입력"
                />
              </label>

              <label>
                이름
                <input
                  name="name"
                  value={userForm.name}
                  onChange={handleUserChange}
                  placeholder="이름"
                />
              </label>

              <label>
                이메일
                <input
                  type="email"
                  name="email"
                  value={userForm.email}
                  onChange={handleUserChange}
                  placeholder="email@example.com"
                />
              </label>

              <label>
                전화번호
                <input
                  name="phone_number"
                  value={userForm.phone_number}
                  onChange={handleUserChange}
                  placeholder="010-1234-5678"
                />
              </label>

              <label>
                성별
                <select name="gender" value={userForm.gender} onChange={handleUserChange}>
                  <option value="M">남성</option>
                  <option value="F">여성</option>
                </select>
              </label>

              <button type="submit">회원가입</button>
              {userMessage && <p className="status-message">{userMessage}</p>}
            </form>
          )}
        </div>
      </div>
    );
  }

  return (
    <div className="page-shell page-two-column">
      <div className="profile-card">
        <div className="profile-header">
          <div className="avatar-wrap">
            {profileForm.profile_image_url ? (
              <img src={profileForm.profile_image_url} alt="profile" className="avatar" />
            ) : (
              <div className="avatar-placeholder">사진</div>
            )}
          </div>
          <div>
            <p className="eyebrow">Wellness</p>
            <h1>Profile</h1>
          </div>
        </div>

        <form onSubmit={handleProfileSubmit} className="profile-form">
          <label>
            닉네임
            <input
              name="nickname"
              value={profileForm.nickname}
              onChange={handleProfileChange}
              placeholder="닉네임을 입력하세요"
            />
          </label>

          <label>
            프로필 이미지 URL
            <input
              name="profile_image_url"
              value={profileForm.profile_image_url}
              onChange={handleProfileChange}
              placeholder="https://..."
            />
          </label>

          <label>
            자기소개
            <textarea
              name="introduction"
              value={profileForm.introduction}
              onChange={handleProfileChange}
              placeholder="자기소개를 입력하세요"
              rows={5}
            />
          </label>

          <button type="submit" disabled={profileLoading}>
            {profileLoading ? "불러오는 중..." : isNewProfile ? "프로필 생성" : "프로필 저장"}
          </button>
        </form>

        {profileMessage && <p className="status-message">{profileMessage}</p>}
      </div>

      <div className="profile-card">
        <div className="profile-header">
          <div className="avatar-wrap user-badge">{currentUser ? currentUser.name[0] : "U"}</div>
          <div>
            <p className="eyebrow">Users</p>
            <h1>Account</h1>
          </div>
        </div>

        <form onSubmit={handleUserUpdate} className="profile-form">
          <label>
            로그인 ID
            <input
              name="login_id"
              value={userForm.login_id}
              onChange={handleUserChange}
              placeholder="login_id"
              disabled
            />
          </label>

          <label>
            이름
            <input
              name="name"
              value={userForm.name}
              onChange={handleUserChange}
              placeholder="이름"
            />
          </label>

          <label>
            이메일
            <input
              type="email"
              name="email"
              value={userForm.email}
              onChange={handleUserChange}
              placeholder="email@example.com"
            />
          </label>

          <label>
            전화번호
            <input
              name="phone_number"
              value={userForm.phone_number}
              onChange={handleUserChange}
              placeholder="010-1234-5678"
            />
          </label>

          <label>
            성별
            <select name="gender" value={userForm.gender} onChange={handleUserChange}>
              <option value="M">남성</option>
              <option value="F">여성</option>
            </select>
          </label>

          <div className="button-row">
            <button type="submit">회원 정보 수정</button>
            <button type="button" className="secondary-button" onClick={handleLogout}>
              로그아웃
            </button>
          </div>
        </form>

        {userMessage && <p className="status-message">{userMessage}</p>}
      </div>

      <div className="profile-card health-card">
        <div className="profile-header">
          <div className="avatar-wrap user-badge">BMI</div>
          <div>
            <p className="eyebrow">Health</p>
            <h1>Metrics</h1>
          </div>
        </div>

        <form onSubmit={handleHealthSubmit} className="profile-form">
          <label>
            키(cm)
            <input
              name="height"
              type="number"
              step="0.1"
              value={healthForm.height}
              onChange={handleHealthChange}
              placeholder="170.2"
            />
          </label>

          <label>
            몸무게(kg)
            <input
              name="weight"
              type="number"
              step="0.1"
              value={healthForm.weight}
              onChange={handleHealthChange}
              placeholder="62.5"
            />
          </label>

          <button type="submit">건강 지표 저장</button>
        </form>

        {healthMessage && <p className="status-message">{healthMessage}</p>}

        <div className="metric-list">
          {healthMetrics.length > 0 ? (
            healthMetrics.map((metric) => (
              <div key={metric.metric_id} className="metric-item">
                <span>{new Date(metric.measured_at).toLocaleString()}</span>
                <strong>
                  {metric.height}cm / {metric.weight}kg
                </strong>
              </div>
            ))
          ) : (
            <p className="empty-state">기록된 건강 지표가 없습니다.</p>
          )}
        </div>
      </div>

      <div className="profile-card health-card">
        <div className="profile-header">
          <div className="avatar-wrap user-badge">⚠</div>
          <div>
            <p className="eyebrow">Constraints</p>
            <h1>Health Limits</h1>
          </div>
        </div>

        <form onSubmit={handleConstraintSubmit} className="profile-form">
          <label>
            제약 유형
            <input
              name="constraint_type"
              value={constraintForm.constraint_type}
              onChange={handleConstraintChange}
              placeholder="예: 알레르기, 질환"
            />
          </label>

          <label>
            제약 내용
            <input
              name="constraint_value"
              value={constraintForm.constraint_value}
              onChange={handleConstraintChange}
              placeholder="예: 견과류, 당뇨"
            />
          </label>

          <button type="submit">제약 조건 저장</button>
        </form>

        {constraintMessage && <p className="status-message">{constraintMessage}</p>}

        <div className="metric-list">
          {constraints.length > 0 ? (
            constraints.map((item) => (
              <div key={item.constraint_id} className="metric-item">
                <span>{new Date(item.created_at).toLocaleDateString()}</span>
                <strong>
                  {item.constraint_type}: {item.constraint_value}
                </strong>
              </div>
            ))
          ) : (
            <p className="empty-state">등록된 제약 조건이 없습니다.</p>
          )}
        </div>
      </div>

      <div className="profile-card health-card">
        <div className="profile-header">
          <div className="avatar-wrap user-badge">🥗</div>
          <div>
            <p className="eyebrow">Diet Plans</p>
            <h1>Meal Plan</h1>
          </div>
        </div>

        <form onSubmit={handleDietPlanSubmit} className="profile-form">
          <label>
            아침
            <input
              name="breakfast"
              value={dietPlanForm.breakfast}
              onChange={handleDietPlanChange}
              placeholder="오트밀"
            />
          </label>

          <label>
            점심
            <input
              name="lunch"
              value={dietPlanForm.lunch}
              onChange={handleDietPlanChange}
              placeholder="닭가슴살 샐러드"
            />
          </label>

          <label>
            저녁
            <input
              name="dinner"
              value={dietPlanForm.dinner}
              onChange={handleDietPlanChange}
              placeholder="연어와 채소"
            />
          </label>

          <button type="submit">식단 플랜 저장</button>
        </form>

        {dietPlanMessage && <p className="status-message">{dietPlanMessage}</p>}

        <div className="metric-list">
          {dietPlans.length > 0 ? (
            dietPlans.map((plan) => (
              <div key={plan.plan_id} className="metric-item plan-item">
                <span>{new Date(plan.created_at).toLocaleDateString()}</span>
                <div>
                  <div>아침: {plan.plan_details.breakfast || "-"}</div>
                  <div>점심: {plan.plan_details.lunch || "-"}</div>
                  <div>저녁: {plan.plan_details.dinner || "-"}</div>
                </div>
              </div>
            ))
          ) : (
            <p className="empty-state">저장된 식단 플랜이 없습니다.</p>
          )}
        </div>
      </div>
    </div>
  );
}

export default App;
