import React from "react";
import { useNavigate } from "react-router";

import { Box, Center } from "@chakra-ui/layout";
import { FormControl, Button } from "@chakra-ui/react";
import { Input, InputGroup } from "@chakra-ui/input";

import { Api } from "../../api/Api";
import { LoginRequest, LoginResponse } from "../../api/types/friendly";
import {
  stateFromAuthenticationResponseData,
  useGlobalState,
} from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";

const Login = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = React.useState("");
  const [passphrase, setPassphrase] = React.useState("");
  const [errorMessage, setErrorMessage] = React.useState("");

  const navigate = useNavigate();

  React.useEffect(() => {
    if (loggedIn(state.credentials!)) {
      navigate("/");
    }
  }, [state.credentials, navigate]);

  const handleErrors = (response: Response) => {
    if (response.status === 401) {
      setErrorMessage("incorrect username or password");
    } else {
      setErrorMessage("something went wrong");
    }
  };

  const postLogin = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    if ([email, passphrase].includes("")) {
      setErrorMessage("cannot be blank");
    } else {
      const request: LoginRequest = { email, passphrase };
      const response: LoginResponse | undefined = await Api().post(
        "identify/login",
        null,
        request,
        handleErrors
      );

      if (response !== undefined) {
        const newState = stateFromAuthenticationResponseData(response);
        setState(newState);
      }
    }
  };

  return (
    <Center h="100%">
      <Box w="container.md">
        <form>
          <FormControl isRequired>
            email
            <InputGroup size="2xl">
              <Input
                autoFocus
                id="login-email"
                type="email"
                borderRadius="lg"
                paddingLeft="4px"
                paddingRight="4px"
                focusBorderColor="black"
                onChange={(event) => {
                  setEmail(event.target.value);
                }}
              />
            </InputGroup>
            password
            <InputGroup size="2xl">
              <Input
                id="login-passphrase"
                type="password"
                borderRadius="lg"
                paddingLeft="4px"
                paddingRight="4px"
                focusBorderColor="black"
                onChange={(event) => {
                  setPassphrase(event.target.value);
                }}
              />
            </InputGroup>
          </FormControl>
          <Button
            id="login-submit"
            width="full"
            type="submit"
            size="2xl" // should try and override Button to add 2xl, removing padding
            borderRadius="lg"
            color="white"
            backgroundColor="black"
            fontWeight="normal"
            paddingBottom="9px"
            paddingTop="3px"
            marginTop="14px"
            loadingText="Logging in..."
            onClick={postLogin}
          >
            Login
          </Button>
          <Center id="login-errorMessage">
            {errorMessage !== "" ? errorMessage : null}
          </Center>
        </form>
      </Box>
    </Center>
  );
};

export default Login;
