import { ArrowForward } from "@mui/icons-material";
import { Button, Chip, Container, Paper, Stack, Typography } from "@mui/material";

export function App() {
  return (
    <Container maxWidth="md" sx={ { py: { xs: 8, md: 14 } } }>
      <Paper elevation={0} sx={ { p: { xs: 4, md: 7 }, border: "1px solid", borderColor: "divider" } }>
        <Stack spacing={3} alignItems="flex-start">
          <Chip label="React + TypeScript" color="primary" variant="outlined" />
          <Typography component="h1" variant="h2" fontWeight={750} letterSpacing="-0.04em">
            Modwire API Browser
          </Typography>
          <Typography variant="h6" color="text.secondary" maxWidth={620}>
            Your application is ready. Replace this starter with the first user journey, then let the tests guide you.
          </Typography>
          <Button variant="contained" size="large" endIcon={<ArrowForward />} href="https://react.dev">
            Explore React
          </Button>
        </Stack>
      </Paper>
    </Container>
  );
}
