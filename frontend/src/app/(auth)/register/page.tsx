import { RegisterForm } from "@/components/auth/RegisterForm";

/**
 * Registration page.
 *
 * Per US1: User can register with email and password.
 */
export default function RegisterPage() {
  return (
    <>
      <div className="mb-8 text-center">
        <h1 className="text-2xl font-bold text-gray-900">Create an account</h1>
        <p className="mt-2 text-sm text-gray-600">
          Start managing your tasks today
        </p>
      </div>
      <RegisterForm />
    </>
  );
}
