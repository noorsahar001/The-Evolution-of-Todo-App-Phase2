/**
 * Auth layout for login and register pages.
 *
 * Provides a centered card layout for authentication forms.
 */
export default function AuthLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <div className="flex min-h-screen items-center justify-center px-4 py-12">
      <div className="w-full max-w-md">
        <div className="rounded-lg bg-white px-8 py-10 shadow-lg">
          {children}
        </div>
      </div>
    </div>
  );
}
