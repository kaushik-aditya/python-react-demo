import React, { Suspense, useState } from "react";
import type { ReactNode, ReactElement } from "react";

type NavbarProps = {
  onToggleSidebar?: () => void;
};

type DefaultLayoutProps = {
  children: ReactNode;
  sidebar: ReactElement;
  navbar: ReactElement<NavbarProps>;
};

const DefaultLayout: React.FC<DefaultLayoutProps> = ({
  children,
  sidebar,
  navbar,
}) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Navbar with injected toggle */}
      <Suspense fallback={<div className="p-4">Loading navbar...</div>}>
        {React.cloneElement(navbar, {
          onToggleSidebar: () => {
            setSidebarOpen((p) => {
              return !p;
            });
          },
        })}
      </Suspense>

      <div className="flex flex-1">
        {/* Sidebar */}
        <Suspense fallback={<div className="p-4">Loading sidebar...</div>}>
          {sidebarOpen && (
            <aside className="w-64 bg-white shadow-md border-r p-4">
              {sidebar}
            </aside>
          )}
        </Suspense>

        {/* Main content */}
        <main className="flex-1 p-4 lg:p-6">
          <Suspense
            fallback={
              <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-4">
                {/* skeleton fallback */}
                {Array.from({ length: 6 }).map((_, i) => (
                  <div
                    key={i}
                    className="border rounded-lg p-4 animate-pulse"
                  >
                    <div className="h-32 bg-gray-300 rounded-md mb-4"></div>
                    <div className="h-4 bg-gray-300 rounded w-3/4 mb-2"></div>
                    <div className="h-4 bg-gray-300 rounded w-1/2"></div>
                  </div>
                ))}
              </div>
            }
          >
            {children}
          </Suspense>
        </main>
      </div>
    </div>
  );
};

export default DefaultLayout;
