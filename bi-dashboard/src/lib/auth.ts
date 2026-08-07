/**
 * auth.ts
 *
 * Lightweight local-only authentication for the MetricMind BI dashboard.
 *
 * No database is required. Credentials are held in-memory during the session
 * and optionally persisted to localStorage when the user selects "Remember me".
 *
 * Demo credentials (for local use only):
 *   email:    demo@axlero.com
 *   password: demo1234
 */

export interface AuthUser {
  name: string;
  email: string;
  role: string;
  initials: string;
}

const SESSION_KEY = "metricmind-session";
const REMEMBER_KEY = "metricmind-remember";
const REMEMBERED_USERNAME_KEY = "metricmind-username";

interface StoredSession {
  user: AuthUser;
  expiresAt: number;
}

const DEMO_USER: AuthUser = {
  name: "Amara Malik",
  email: "demo@axlero.com",
  role: "Finance Director",
  initials: "AM",
};

const SESSION_MS = 1000 * 60 * 60 * 8; // 8 hours

function buildUser(email: string): AuthUser {
  const name = email === "demo@axlero.com" ? DEMO_USER.name : email.split("@")[0];
  const initials = name
    .split(/\s+/)
    .slice(0, 2)
    .map((part) => part[0]?.toUpperCase() ?? "")
    .join("");

  return {
    name,
    email,
    role: name === DEMO_USER.name ? DEMO_USER.role : "Analyst",
    initials: initials || "U",
  };
}

/**
 * Validate credentials against the local demo account.
 * Returns the authenticated user or throws on failure.
 */
export function loginWithEmailPassword(
  email: string,
  password: string,
  remember: boolean,
): AuthUser {
  const normalized = email.trim().toLowerCase();
  const now = Date.now();

  // Simulate a network/auth round-trip boundary.
  if (!normalized || !password) {
    throw new Error("Please enter both email and password.");
  }

  const validUser = normalized === "demo@axlero.com";
  const validPassword = password === "demo1234";

  if (!validUser || !validPassword) {
    throw new Error("Invalid email or password. Try demo@axlero.com / demo1234.");
  }

  const user = buildUser(normalized);

  if (remember) {
    window.localStorage.setItem(REMEMBERED_USERNAME_KEY, normalized);
    window.localStorage.setItem(
      REMEMBER_KEY,
      JSON.stringify({
        email: normalized,
        expiresAt: now + SESSION_MS,
        user,
      }),
    );
  } else {
    window.localStorage.removeItem(REMEMBER_KEY);
  }

  // Session persistence always has an in-memory + sessionStorage copy so the
  // active login survives tab refreshes during the current browser session.
  window.sessionStorage.setItem(
    SESSION_KEY,
    JSON.stringify({ user, expiresAt: now + SESSION_MS } satisfies StoredSession),
  );

  return user;
}

/**
 * Restore the active session (sessionStorage or remembered localStorage).
 * Returns the user or null when no valid session exists.
 */
export function restoreSession(): AuthUser | null {
  if (typeof window === "undefined") {
    return null;
  }

  const now = Date.now();

  const readSession = (raw: string | null): StoredSession | null => {
    if (!raw) {
      return null;
    }

    try {
      const parsed = JSON.parse(raw) as StoredSession;

      if (!parsed.user || typeof parsed.expiresAt !== "number") {
        return null;
      }

      if (parsed.expiresAt < now) {
        return null;
      }

      return parsed;
    } catch {
      return null;
    }
  };

  const session = readSession(window.sessionStorage.getItem(SESSION_KEY));

  if (session) {
    return session.user;
  }

  const rememberedRaw = window.localStorage.getItem(REMEMBER_KEY);

  if (rememberedRaw) {
    try {
      const remembered = JSON.parse(rememberedRaw) as {
        email: string;
        expiresAt: number;
        user: AuthUser;
      };

      if (remembered.expiresAt < now) {
        window.localStorage.removeItem(REMEMBER_KEY);
        return null;
      }

      // Re-establish a fresh sessionStorage entry so the session persists.
      window.sessionStorage.setItem(
        SESSION_KEY,
        JSON.stringify({
          user: remembered.user,
          expiresAt: now + SESSION_MS,
        } satisfies StoredSession),
      );

      return remembered.user;
    } catch {
      return null;
    }
  }

  return null;
}

/** Clear the active session locally. */
export function logout(): void {
  window.sessionStorage.removeItem(SESSION_KEY);
  window.localStorage.removeItem(REMEMBER_KEY);
}

/** Whether a remembered email is stored (pre-fills the login form). */
export function getRememberedEmail(): string | null {
  return window.localStorage.getItem(REMEMBERED_USERNAME_KEY);
}

