import { Button } from "@chakra-ui/react";
import { MouseEventHandler } from "react";

interface RightPaginationControlProps {
    disabled: boolean;
    onClick: MouseEventHandler<HTMLButtonElement>;
}

const RightPaginationControl = (props: RightPaginationControlProps) => {
    const { disabled, onClick } = props;

    return (
        <Button disabled={disabled} onClick={onClick}>&#62;</Button>
    );
}

export { RightPaginationControl };
