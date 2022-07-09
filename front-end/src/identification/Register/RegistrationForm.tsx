import { useNavigate } from "react-router";
import { useEffect, useState } from "react";

import { useGlobalState } from "../../GlobalState";

import { Role } from "../../datatypes/Role";
import { User } from "../../datatypes/User";


interface RegistrationPayload {
  email: String;
}

const RegistrationForm = () => {
  const { state, setState } = useGlobalState();
  const [email, setEmail] = useState('');
  const navigate = useNavigate();

  useEffect(() => {
    if (state.roles!.length > 0) {
      navigate("/");
    }
  }, [state, navigate])

  const register = async (event: React.MouseEvent<HTMLFormElement>) => {
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
    <form onSubmit={register}>
      <label>
        email:{" "}
        <input type="text" name="email" onChange={(event) => { setEmail(event.target.value) }} />
      </label>{" "}
      <input type="submit" value="Submit" />
    </form>
  );
}

export { RegistrationForm };