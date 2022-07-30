import React from "react";

import { useNavigate } from "react-router";

import { Box, Center } from "@chakra-ui/layout";
import { FormControl, Button } from '@chakra-ui/react';
import { Input, InputGroup } from "@chakra-ui/input";

import { Api } from "../../api/Api";
import { RegisterRequest, RegisterResponse } from "../../api/types/friendly";
import { stateFromAuthenticationResponseData, useGlobalState } from "../../GlobalState";
import { loggedIn } from "../../utility/authorization";


const Register = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = React.useState('');
  const [passphrase, setPassphrase] = React.useState('');
  const [verification, setVerification] = React.useState('');
  const [errorMessage, setErrorMessage] = React.useState('');

  const navigate = useNavigate();

  React.useEffect(() => {
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
      const response: RegisterResponse | undefined = await Api().post('identify/register', null, request, handleErrors)
      
      if (response !== undefined) {
        const newState = stateFromAuthenticationResponseData(response);
        setState(newState);
      }
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
                id='register-email'
                type='email'
                borderRadius="lg"
                paddingLeft="4px"
                paddingRight="4px"
                focusBorderColor="black"
                onChange={(event) => { setEmail(event.target.value) }}
              />
            </InputGroup>
            password
            <InputGroup size='2xl'>
              <Input
                id='register-passphrase'
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
                id='register-verification'
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
            id='register-submit'
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
          <Center id='register-errorMessage'>{errorMessage !== '' ? errorMessage : null}</Center>
        </form>
      </Box>
    </Center>
  );
}

export { Register };
