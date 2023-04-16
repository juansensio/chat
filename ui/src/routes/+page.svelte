<script>
  import { PUBLIC_API_URL } from "$env/static/public";
  let prompt = "";
  let prompts = [];
  let responses = [];
  let loading = false;
  let current_response = "";
  const generate = async () => {
    if (!prompt || prompt.length == 0) return;
    prompts = [...prompts, prompt];
    loading = true;
    prompt = "";
    current_response = "Loading...";
    const request_prompt = prompts
      .map((p, i) => {
        if (i < prompts.length - 1)
          return (
            p +
            "<|endoftext|><|assistant|>" +
            responses[i] +
            "<|endoftext|><|prompter|>"
          );
        return p;
      })
      .join(" ");
    const res = await fetch(PUBLIC_API_URL, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({ prompt: request_prompt }),
    });
    const reader = res.body.getReader();
    const decoder = new TextDecoder("utf-8");
    let text = "";
    const read = async () => {
      const { done, value } = await reader.read();
      if (done) return;
      text = decoder.decode(value);
      current_response = text;
      await read();
    };
    await read();
    responses = [...responses, text];
    current_response = "";
    loading = false;
  };
</script>

<main class="p-3 flex flex-col w-full h-screen justify-between">
  <div>
    <h1 class="text-3xl font-bold">ChatGPT clone</h1>
    <div class="overflow-auto">
      {#each prompts as prompt, i}
        <div class="p-2 rounded-lg">{prompt}</div>
        {#if i == prompts.length - 1 && current_response.length > 0}
          <div class="bg-gray-200 p-2 rounded-lg">{current_response}</div>
        {:else}
          <div class="bg-gray-200 p-2 rounded-lg">{responses[i]}</div>
        {/if}
      {/each}
    </div>
  </div>
  <form on:submit|preventDefault={generate} class="flex flex-row gap-3 mt-3">
    <input
      type="text"
      class="border border-2-gray p-2 w-full"
      placeholder="Prompt..."
      bind:value={prompt}
    />
    <button
      disabled={loading}
      type="submit"
      class="border border-2-gray p-2 {loading ? 'bg-gray-200' : ''}}"
      >Generate</button
    >
  </form>
</main>
