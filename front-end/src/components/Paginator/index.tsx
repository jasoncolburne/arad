import { HStack } from '@chakra-ui/react';
import { ReactNode } from 'React';

import { PaginationControl } from './components/PaginationControl';


interface PaginatorProps {
    page: number;
    total: number;
    setPage: Function;
    children: ReactNode;
};

const Paginator = (props: PaginatorProps) => {
    const { page, total, setPage, children } = props;

    return (
        <HStack verticalAlign='center'>
            <PaginationControl content='<' disabled={page <= 1} onClick={(event) => { setPage(page - 1); }} />
            {children}
            <PaginationControl content='>' disabled={page >= total - 1} onClick={(event) => { setPage(page + 1); }} />
        </HStack>
    );
};

export { Paginator };
