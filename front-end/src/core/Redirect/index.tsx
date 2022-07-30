import React from "react";
import { Center } from "@chakra-ui/layout";
import { ChakraProvider, theme } from "@chakra-ui/react";

interface RedirectProps {
  url: string;
}

const Redirect = (props: RedirectProps) => {
  const { url } = props;

  React.useEffect(() => {
    window.location.replace(url);
  }, [url]);

  return (
    <ChakraProvider theme={theme}>
      <Center h="100%">Redirecting to {url}...</Center>
    </ChakraProvider>
  );
};

export { Redirect };
