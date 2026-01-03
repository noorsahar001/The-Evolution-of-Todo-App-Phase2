import { redirect } from "next/navigation";

/**
 * Home page - redirects to dashboard or login.
 *
 * Per FR-008: Unauthenticated users should be redirected to login.
 * The actual auth check is handled by middleware.
 */
export default function Home() {
  // Redirect to dashboard - middleware will handle auth check
  redirect("/dashboard");
}
