import { Alert, Group, Stack } from '@mantine/core';
import Image from 'next/image';
import logo from '../public/orange.png';
import replylogo from '../public/purple.png';

const ChatMessage = (props: any) => {
  const { text, user } = props;
  const message = user ? 'right' : 'left';
  let color;

  if (message === 'right') {
    color = 'indigo';
  }
  if (message === 'left') {
    color = 'yellow';
  }

  return (
    <>
      <Group justify={message} align="flex-end">
        <Stack p={0} align="flex-end">
          <Group justify={message} align="flex-end" wrap="nowrap">
            <Image
              src={logo}
              height={35}
              width={30}
              alt="CommentSense Bot"
              hidden={message === 'right' ? true : false}
            />
            <Stack p={0} m={0}>
              <Group justify={message} align="center">
                <Alert color={color} radius="lg" py={8} variant="light">
                  {text}
                </Alert>
              </Group>
            </Stack>
            <Image
              src={replylogo}
              height={35}
              width={30}
              alt="Prompter Logo"
              hidden={message === 'right' ? false : true}
            />
          </Group>
        </Stack>
      </Group>
    </>
  );
};

export default ChatMessage;
