import React, { useState } from "react";

type Props = {
  children: React.ReactNode;
  sidebar: React.ReactNode;
  navbar: React.ReactElement<{ onToggleSidebar?: () => void }>; 
  // 👆 explicitly say Navbar accepts optional onToggleSidebar
};

const DefaultLayout: React.FC<Props> = ({ children, sidebar, navbar }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);

  return (
    <div className="min-h-screen flex flex-col bg-gray-50">
      {/* Navbar with injected toggle */}
      {React.cloneElement(navbar, {
        onToggleSidebar: () => setSidebarOpen((p) => !p),
      })}

      <div className="flex flex-1">
        {/* Sidebar */}
        {sidebarOpen && (
          <aside className="w-64 bg-white shadow-md border-r p-4">
            {sidebar}
          </aside>
        )}

        {/* Main content */}
        <main className="flex-1 p-4 lg:p-6">{children}</main>
      </div>
    </div>
  );
};

export default DefaultLayout;
