import { LoginForm } from "@/components/auth/LoginForm";

/**
 * Login page.
 *
 * Per US2: User can login with email and password.
 */
export default function LoginPage() {
  return (
    <>
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold text-gray-900">Welcome back</h1>
        <p className="mt-2 text-sm text-gray-600">
          Sign in to access your tasks
        </p>
      </div>
      <LoginForm />
    </>
  );
}
