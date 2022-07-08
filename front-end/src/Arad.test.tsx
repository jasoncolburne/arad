import { render, screen } from '@testing-library/react';
import { Arad } from './Arad';

test('renders learn react link', () => {
  render(<Arad />);
  const linkElement = screen.getByText(/ARAD: Accessible Research Article Database/);
  expect(linkElement).toBeInTheDocument();
});
