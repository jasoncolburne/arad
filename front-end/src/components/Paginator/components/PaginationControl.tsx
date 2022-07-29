import { Button } from "@chakra-ui/react";
import { MouseEventHandler } from "react";

interface PaginationControlProps {
    content: string;
    disabled: boolean;
    onClick: MouseEventHandler<HTMLButtonElement>;
}

const PaginationControl = (props: PaginationControlProps) => {
    const { content, disabled, onClick } = props;

    return (
        <Button verticalAlign='center' disabled={disabled} onClick={onClick}>{content}</Button>
    );
}

export { PaginationControl };
