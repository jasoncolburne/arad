const randomEmail = (prefix: string = 'user', domain: string = 'domain.org') => {
    const randomId = Math.ceil(Math.random() * 1000000);
    return `${prefix}+${randomId}@${domain}`;
};

export { randomEmail };