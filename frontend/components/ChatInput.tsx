import React from 'react';
import { TextInput, TextInputProps, ActionIcon, useMantineTheme, rem } from '@mantine/core';
import { IconArrowRight } from '@tabler/icons-react';
import { Dispatch, SetStateAction } from 'react';
import { getHotkeyHandler } from '@mantine/hooks';

interface ExtendedTextInputProps extends TextInputProps {
  fn: () => void;
  addMessage: (mess: string) => void;
  setValue: Dispatch<SetStateAction<string>>;
  value: string;
}

export function ChatInput(props: ExtendedTextInputProps) {
  const { fn, addMessage, setValue, value, ...textInputProps } = props;
  const theme = useMantineTheme();

  const sendMessage = async () => {
    if (value.length <= 1) {
      return;
    } else {
      fn();
      addMessage(value);
      setValue('');
    }
  };

  return (
    <div
      style={{
        display: 'flex',
        flexDirection: 'column', // Align items in a column
        justifyContent: 'flex-end',
        padding: '10px',
      }}
    >
      <div style={{ marginBottom: '1rem' }}>
        <TextInput
          radius="xl"
          size="md"
          placeholder="Message CommentSense!"
          value={value}
          onChange={(event) => setValue(event.currentTarget.value)}
          rightSectionWidth={42}
          rightSection={
            <ActionIcon
              size={32}
              radius="xl"
              color={theme.primaryColor}
              variant="filled"
              onClick={sendMessage}
              style={{ cursor: 'pointer' }}
            >
              <IconArrowRight style={{ width: rem(18), height: rem(18) }} stroke={1.5} />
            </ActionIcon>
          }
          onKeyDown={
            !/\S/.test(value)
              ? undefined
              : value.length < 2
                ? undefined
                : getHotkeyHandler([['Enter', sendMessage]])
          }
          {...textInputProps}
        />
      </div>
    </div>
  );
}

export default ChatInput;
