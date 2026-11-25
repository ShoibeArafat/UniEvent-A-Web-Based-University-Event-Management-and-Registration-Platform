import React, { useState } from "react"
import { useAuth } from "../context/AuthContext"
import { BuildingIcon, SparklesIcon } from "../components/Icons"
import "./Login.css"

interface LoginProps {
  onSuccess?: () => void
}

export default function Login({ onSuccess }: LoginProps) {
  const { login, signup } = useAuth()
  const [mode, setMode] = useState<"login" | "signup">("login")

  // Login form state
  const [loginEmail, setLoginEmail] = useState("")
  const [loginPassword, setLoginPassword] = useState("")

  // Signup form state
  const [signupName, setSignupName] = useState("")
  const [signupEmail, setSignupEmail] = useState("")
  const [signupPassword, setSignupPassword] = useState("")
  const [signupConfirm, setSignupConfirm] = useState("")

  // Status
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState<string | null>(null)

  const handleTabSwitch = (newMode: "login" | "signup") => {
    setMode(newMode)
    setError(null)
  }

  const fillDemoAccount = (email: string, pass: string) => {
    setMode("login")
    setLoginEmail(email)
    setLoginPassword(pass)
    setError(null)
  }

  const handleLoginSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)
    setLoading(true)
    try {
      await login(loginEmail, loginPassword)
      onSuccess?.()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Invalid credentials. Please verify your email and password.")
    } finally {
      setLoading(false)
    }
  }

  const handleSignupSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    setError(null)

    if (signupPassword.length < 6) {
      setError("Password must be at least 6 characters long.")
      return
    }

    if (signupPassword !== signupConfirm) {
      setError("Passwords do not match.")
      return
    }

    setLoading(true)
    try {
      await signup(signupName, signupEmail, signupPassword)
      onSuccess?.()
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to register account.")
    } finally {
      setLoading(false)
    }
  }

  return (
    <main className="login-page-wrapper">
      <div className="login-page-card">
        {/* Brand Header */}
        <div className="login-brand-header">
          <div className="login-brand-logo">
            <BuildingIcon width={26} height={26} />
          </div>
          <div>
            <h1 className="login-brand-title">UniEvent</h1>
            <p className="login-brand-subtitle">University Event Management Platform</p>
          </div>
        </div>

        {/* Tab Switcher */}
        <div className="login-tab-row">
          <button
            type="button"
            className={`login-tab-btn ${mode === "login" ? "active" : ""}`}
            onClick={() => handleTabSwitch("login")}
          >
            Sign In
          </button>
          <button
            type="button"
            className={`login-tab-btn ${mode === "signup" ? "active" : ""}`}
            onClick={() => handleTabSwitch("signup")}
          >
            Create Account
          </button>
        </div>

        {/* Error Alert */}
        {error && (
          <div className="login-error-alert" role="alert">
            {error}
          </div>
        )}

        {/* Demo Quick-Fill for Teacher Assessment */}
        {mode === "login" && (
          <div className="login-demo-box">
            <div className="login-demo-header">
              <SparklesIcon width={14} height={14} />
              <span>Quick Demo Login (Teacher Viva):</span>
            </div>
            <div className="login-demo-pills">
              <button
                type="button"
                className="demo-pill-btn"
                onClick={() => fillDemoAccount("admin1@unievent.edu", "Admin@12345")}
              >
                Admin (admin1)
              </button>
              <button
                type="button"
                className="demo-pill-btn"
                onClick={() => fillDemoAccount("admin2@unievent.edu", "Admin@12345")}
              >
                Admin 2 (admin2)
              </button>
              <button
                type="button"
                className="demo-pill-btn"
                onClick={() => fillDemoAccount("student@unievent.edu", "User@12345")}
              >
                Student (student)
              </button>
              <button
                type="button"
                className="demo-pill-btn"
                onClick={() => fillDemoAccount("student2@unievent.edu", "Tanvir#2026!")}
              >
                Student 2 (Tanvir)
              </button>
              <button
                type="button"
                className="demo-pill-btn"
                onClick={() => fillDemoAccount("student3@unievent.edu", "Nafis@Pass99")}
              >
                Student 3 (Nafis)
              </button>
              <button
                type="button"
                className="demo-pill-btn"
                onClick={() => fillDemoAccount("student4@unievent.edu", "Sadia*Secure1")}
              >
                Student 4 (Sadia)
              </button>
            </div>
          </div>
        )}

        {/* Sign In Form */}
        {mode === "login" ? (
          <form onSubmit={handleLoginSubmit} className="modal-form">
            <div className="form-group">
              <label htmlFor="login-email">University Email</label>
              <input
                id="login-email"
                type="email"
                className="form-input"
                placeholder="you@unievent.edu"
                value={loginEmail}
                onChange={(e) => setLoginEmail(e.target.value)}
                required
                autoComplete="email"
              />
            </div>

            <div className="form-group">
              <label htmlFor="login-password">Password</label>
              <input
                id="login-password"
                type="password"
                className="form-input"
                placeholder="••••••••"
                value={loginPassword}
                onChange={(e) => setLoginPassword(e.target.value)}
                required
                autoComplete="current-password"
              />
            </div>

            <button type="submit" className="btn btn-primary btn-block py-3 mt-2" disabled={loading}>
              {loading ? "Authenticating..." : "Sign In to Dashboard"}
            </button>
          </form>
        ) : (
          /* Sign Up Form */
          <form onSubmit={handleSignupSubmit} className="modal-form">
            <div className="form-group">
              <label htmlFor="signup-name">Full Name</label>
              <input
                id="signup-name"
                type="text"
                className="form-input"
                placeholder="Shoibe Arafat"
                value={signupName}
                onChange={(e) => setSignupName(e.target.value)}
                required
              />
            </div>

            <div className="form-group">
              <label htmlFor="signup-email">University Email</label>
              <input
                id="signup-email"
                type="email"
                className="form-input"
                placeholder="student@unievent.edu"
                value={signupEmail}
                onChange={(e) => setSignupEmail(e.target.value)}
                required
                autoComplete="email"
              />
            </div>

            <div className="form-row">
              <div className="form-group">
                <label htmlFor="signup-password">Password</label>
                <input
                  id="signup-password"
                  type="password"
                  className="form-input"
                  placeholder="••••••••"
                  value={signupPassword}
                  onChange={(e) => setSignupPassword(e.target.value)}
                  required
                  minLength={6}
                  autoComplete="new-password"
                />
              </div>

              <div className="form-group">
                <label htmlFor="signup-confirm">Confirm Password</label>
                <input
                  id="signup-confirm"
                  type="password"
                  className="form-input"
                  placeholder="••••••••"
                  value={signupConfirm}
                  onChange={(e) => setSignupConfirm(e.target.value)}
                  required
                  minLength={6}
                  autoComplete="new-password"
                />
              </div>
            </div>

            <button type="submit" className="btn btn-primary btn-block py-3 mt-2" disabled={loading}>
              {loading ? "Creating Account..." : "Register & Continue"}
            </button>
          </form>
        )}
      </div>
    </main>
  )
}
