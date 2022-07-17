import { useEffect, useState } from "react";
import { useNavigate } from "react-router";

import { Box, Center } from "@chakra-ui/layout";
import { FormControl, Button } from '@chakra-ui/react';
import { Input, InputGroup } from "@chakra-ui/input";

import { Api } from "../../api/Api";
import { RegisterResponse } from "../../api/types/friendly";
import { ApplicationState } from "../../datatypes/ApplicationState";
import { useGlobalState } from "../../GlobalState";


interface RegistrationPayload {
  email: String;
  passphrase: String;
}

const Register = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = useState('');
  const [passphrase, setPassphrase] = useState('');
  const [verification, setVerification] = useState('');
  const [errorMessage, setErrorMessage] = useState('');

  const navigate = useNavigate();
  const loggedIn = state.roles!.length > 0;

  useEffect(() => {
    if (loggedIn) {
      navigate("/");
    }
  }, [loggedIn, navigate])

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
      const payload: RegistrationPayload = { email, passphrase };
      const response: RegisterResponse = await Api().post('identify/register', null, payload, handleErrors)
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
