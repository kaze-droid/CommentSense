import { Center, Group, Kbd, Loader, Stack, Text } from "@mantine/core";

const Loading = () => {
  return (
    <Center>
      <Stack align="center" >
        <Text>Stuck on loading? just press</Text>
        <Group>
          <Kbd>ctrl</Kbd> + <Kbd>R</Kbd>
        </Group>

        <Loader color="grape" />
      </Stack>
    </Center>
  );
};

export default Loading;
