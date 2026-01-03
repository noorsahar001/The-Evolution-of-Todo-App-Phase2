import { NextResponse } from "next/server";
import type { NextRequest } from "next/server";

/**
 * Middleware to protect authenticated routes.
 *
 * Per FR-008: Redirect unauthenticated users from protected pages to login.
 *
 * Note: This is a simplified check. The actual JWT validation happens on the backend.
 * The cookie presence is just a hint for routing - the backend is the source of truth.
 */
export function middleware(request: NextRequest) {
  const { pathname } = request.nextUrl;

  // Check for auth cookie
  const hasAuthCookie = request.cookies.has("access_token");

  // Protected routes require authentication
  const protectedRoutes = ["/dashboard"];
  const isProtectedRoute = protectedRoutes.some((route) =>
    pathname.startsWith(route)
  );

  // Auth routes should redirect to dashboard if already logged in
  const authRoutes = ["/login", "/register"];
  const isAuthRoute = authRoutes.some((route) => pathname.startsWith(route));

  // Redirect unauthenticated users from protected routes to login
  if (isProtectedRoute && !hasAuthCookie) {
    return NextResponse.redirect(new URL("/login", request.url));
  }

  // Redirect authenticated users from auth routes to dashboard
  if (isAuthRoute && hasAuthCookie) {
    return NextResponse.redirect(new URL("/dashboard", request.url));
  }

  return NextResponse.next();
}

export const config = {
  matcher: ["/dashboard/:path*", "/login", "/register"],
};
