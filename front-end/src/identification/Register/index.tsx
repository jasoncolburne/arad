import { useNavigate } from "react-router";
import { useEffect, useState } from "react";

import {
  Input,
  InputGroup,
} from "@chakra-ui/input";

import {
  FormControl,
  Button,
} from '@chakra-ui/react';

import { useGlobalState } from "../../GlobalState";

import { Role } from "../../datatypes/Role";
import { User } from "../../datatypes/User";
import { Box, Center, Stack } from "@chakra-ui/layout";


interface RegistrationPayload {
  email: String;
}

const Register = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (state.roles!.length > 0) {
      navigate("/");
    }
  }, [state, navigate])

  const postRegistration = async (event: React.MouseEvent<HTMLButtonElement>) => {
    event.preventDefault();
    const payload: RegistrationPayload = { email };
    const response = await fetch('http://localhost:81/identify/register', {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify(payload)
    });
    const user: User = await response.json();
    const newState = { ...state, user, roles: [Role.Reader] };
    setState(newState);
  }

  return (
    <Center h="100%">
      <Box w="container.md">
        <FormControl isRequired>
          Email:
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
        </FormControl>
        <Button
          width="full"
          type="submit"
          size="2xl"
          borderRadius="lg"
          color="white"
          backgroundColor="black"
          fontWeight="normal"
          paddingBottom="7px"
          onClick={postRegistration}
        >
          Register
        </Button>
      </Box>
    </Center>
  );
}

export { Register };
