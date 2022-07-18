import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import { Box, Center } from "@chakra-ui/layout";
import { FormControl, Button } from '@chakra-ui/react';
import { Input, InputGroup } from "@chakra-ui/input";

import { Api } from "../../api/Api";
import { RegisterRequest, RegisterResponse } from "../../api/types/friendly";
import { ApplicationState } from "../../datatypes/ApplicationState";
import { useGlobalState } from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";
import { emptyCredentials } from "../../datatypes/Credentials";


const Register = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = useState('');
  const [passphrase, setPassphrase] = useState('');
  const [verification, setVerification] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();

  useEffect(() => {
    if (loggedIn(state.credentials!)) {
      navigate("/");
    }
  }, [state.credentials, navigate])

  const handleErrors = (response: Response) => {
    if (response.status === 400) {
      setErrorMessage('please enter a valid email address')
    } else {
      setErrorMessage(`something went wrong: ${response.status}`);
    }
  };

  const postRegistration = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    if (passphrase !== verification) {
      setErrorMessage('passphrases must match');
    } else if ([email, passphrase, verification].includes('')) {
      setErrorMessage('cannot be blank');
    } else {
      const request: RegisterRequest = { email, passphrase };
      const response: RegisterResponse = await Api().post('identify/register', null, request, handleErrors)
      const newState: ApplicationState = {
        ...state,
        credentials: {
          ...emptyCredentials,
          refresh_token: response.refresh_token,
        },
        user: response.user,
        roles: response.roles,
      };
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
            verification
            <InputGroup size='2xl'>
              <Input
                id='verification'
                type='password'
                borderRadius="lg"
                paddingLeft="4px"
                paddingRight="4px"
                focusBorderColor="black"
                onChange={(event) => { setVerification(event.target.value) }}
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
            loadingText="Registering..."
            onClick={postRegistration}
          >
            Register
          </Button>
          <Center>{errorMessage !== '' ? errorMessage : null}</Center>
        </form>
      </Box>
    </Center>
  );
}

export { Register };
