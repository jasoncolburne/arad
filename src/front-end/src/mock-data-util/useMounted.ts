import { useEffect, useRef } from "react";
import type { MutableRefObject } from "react";

const useMounted = (): MutableRefObject<boolean> => {
  const isMounted = useRef(true);

  // sets up a cleanup to prevent memory leak.
  // when component unmounts, set ref current to false
  useEffect(
    () => (): void => {
      setTimeout(() => {
        isMounted.current = false;
      }, 0)
    },
    []
  );

  return isMounted;
};

export default useMounted;