import React from "react";

import { render, screen } from '@testing-library/react';
import { Arad } from './Arad';

test('renders name', () => {
  render(<Arad />);
  const linkElement = screen.getByText(/Accessible Research Article Database/);
  expect(linkElement).toBeInTheDocument();
});
