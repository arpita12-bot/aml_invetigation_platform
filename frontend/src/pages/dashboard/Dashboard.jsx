import { Container, Typography } from "@mui/material";

export default function Dashboard() {
  return (
    <Container sx={{ mt: 5 }}>
      <Typography variant="h4">
        AML Investigation Dashboard
      </Typography>

      <Typography>
        Phase 7 Successfully Started
      </Typography>
    </Container>
  );
}