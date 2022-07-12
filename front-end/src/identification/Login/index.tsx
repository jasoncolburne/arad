import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import { Box, Center } from "@chakra-ui/layout";
import { FormControl, Button } from '@chakra-ui/react';
import { Input, InputGroup } from "@chakra-ui/input";

import { Api } from "../../api/Api";
import { ApplicationState } from "../../datatypes/ApplicationState";
import { useGlobalState } from "../../GlobalState";

interface LoginPayload {
  email: String;
  passphrase: String;
}

const Login = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = useState('');
  const [passphrase, setPassphrase] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();
  const loggedIn = state.roles!.length > 0;

  useEffect(() => {
    if (loggedIn) {
      navigate("/");
    }
  }, [loggedIn, navigate])

  const handleErrors = (response: Response) => {
    if ([401, 403].includes(response.status)) {
      setErrorMessage('incorrect username or password');
    } else {
      setErrorMessage('something went wrong');
    }
  };

  const postLogin = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    if ([email, passphrase].includes('')) {
    } else {
      const payload: LoginPayload = { email, passphrase };
      const response: ApplicationState = await Api().post('identify/login', null, payload, handleErrors);
      const newState: ApplicationState = { ...state, ...response };
      setState(newState);
    }
  }

  return (
    <Center h="100%">
      <Box w="container.md">
        <form>
          <FormControl isRequired>
            email
            <InputGroup size='2xl'>
              <Input
                id='email'
                type='email'
                borderRadius="lg"
                paddingLeft="4px"
                paddingRight="4px"
                focusBorderColor="black"
                onChange={(event) => { setEmail(event.target.value) }}
              />
            </InputGroup>
            passphrase
            <InputGroup size='2xl'>
              <Input
                id='passphrase'
                type='password'
                borderRadius="lg"
                paddingLeft="4px"
                paddingRight="4px"
                focusBorderColor="black"
                onChange={(event) => { setPassphrase(event.target.value) }}
              />
            </InputGroup>
          </FormControl>
          <Button
            width="full"
            type="submit"
            size="2xl"  // should try and override Button to add 2xl, removing padding
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
          <Center>{errorMessage !== '' ? errorMessage : null}</Center>
        </form>
      </Box>
    </Center>
  );
}

export { Login };
