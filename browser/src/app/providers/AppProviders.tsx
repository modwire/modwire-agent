import { MantineProvider } from "@mantine/core";
import { Notifications } from "@mantine/notifications";
import { QueryClient, QueryClientProvider } from "@tanstack/react-query";
import { useState, type ReactNode } from "react";

type AppProvidersProps = {
  children: ReactNode;
};

export function AppProviders({ children }: AppProvidersProps): ReactNode {
  const [queryClient] = useState(() => new QueryClient());

  return (
    <MantineProvider>
      <QueryClientProvider client={queryClient}>
        <Notifications />
        {children}
      </QueryClientProvider>
    </MantineProvider>
  );
}
