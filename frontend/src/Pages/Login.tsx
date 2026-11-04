import { useState } from "react";
import type { FormEvent } from "react";
import "./login.css";

const API_URL: string = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

interface LoginResponse {
  access_token: string;
}

interface LoginProps {
  onSuccess?: () => void;
}

interface FieldErrors {
  email?: string;
  password?: string;
}

async function loginRequest(email: string, password: string): Promise<LoginResponse> {
  const res = await fetch(`${API_URL}/api/auth/login`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ email, password }),
  });
  if (!res.ok) {
    if (res.status === 401) throw new Error("Email or password is incorrect.");
    throw new Error("Could not sign in. Try again in a moment.");
  }
  return res.json();
}

export default function Login({ onSuccess }: LoginProps) {
  const [email, setEmail] = useState<string>("");
  const [password, setPassword] = useState<string>("");
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [errors, setErrors] = useState<FieldErrors>({});
  const [formError, setFormError] = useState<string>("");
  const [loading, setLoading] = useState<boolean>(false);

  const handleSubmit = async (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    setFormError("");

    const next: FieldErrors = {};
    if (!email.trim()) next.email = "Enter your university email.";
    else if (!/^\S+@\S+\.\S+$/.test(email)) next.email = "Enter a valid email address.";
    if (!password) next.password = "Enter your password.";
    setErrors(next);
    if (Object.keys(next).length > 0) return;

    setLoading(true);
    try {
      const data = await loginRequest(email.trim(), password);
      localStorage.setItem("access_token", data.access_token);
      onSuccess?.();
    } catch (err) {
      setFormError(err instanceof Error ? err.message : "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <main className="login">
      <form className="login__card" onSubmit={handleSubmit} noValidate>
        <h1>Sign in</h1>
        <p className="login__sub">Use your university account to browse and manage events.</p>

        {formError && (
          <div className="login__alert" role="alert">
            {formError}
          </div>
        )}

        <div className="field">
          <label htmlFor="email">University email</label>
          <input
            id="email"
            type="email"
            autoComplete="email"
            placeholder="you@university.edu"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            aria-invalid={!!errors.email}
          />
          {errors.email && <span className="field__error">{errors.email}</span>}
        </div>

        <div className="field">
          <label htmlFor="password">Password</label>
          <div className="field__password">
            <input
              id="password"
              type={showPassword ? "text" : "password"}
              autoComplete="current-password"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              aria-invalid={!!errors.password}
            />
            <button
              type="button"
              className="field__toggle"
              onClick={() => setShowPassword((s) => !s)}
              aria-pressed={showPassword}
            >
              {showPassword ? "Hide" : "Show"}
            </button>
          </div>
          {errors.password && <span className="field__error">{errors.password}</span>}
        </div>

        <button className="login__submit" type="submit" disabled={loading}>
          {loading ? "Signing in…" : "Sign in"}
        </button>

        <p className="login__footer">
          New to UniEvent? <a href="/register">Create an account</a>
        </p>
      </form>
    </main>
  );
}
