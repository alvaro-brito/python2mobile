# P2M Imagine - Code Generation Guide

## Overview

The `p2m imagine` command generates Python2Mobile applications from natural language descriptions using LLM providers. This allows you to describe what you want to build and automatically generate production-ready P2M code.

## Quick Start

### Basic Usage

```bash
p2m imagine "Create a Hello World app with a button"
```

### With Ollama (Local)

```bash
p2m imagine "Create a Todo app" --provider ollama --base-url http://localhost:11434 --model qwen3-coder:latest
```

### With OpenAI

```bash
export OPENAI_API_KEY="sk-..."
p2m imagine "Create a counter app with increment and decrement buttons"
```

### With Anthropic (Claude)

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
p2m imagine "Create a contact form" --provider anthropic
```

### With Custom OpenAI-Compatible API

```bash
p2m imagine "Create a dashboard" \
  --provider openai-compatible \
  --base-url https://api.example.com/v1 \
  --api-key your-api-key \
  --model your-model-name
```

## Command Options

### Provider Selection

```bash
--provider [openai|anthropic|ollama|openai-compatible]
```

Default: `openai`

### Model Selection

```bash
--model MODEL_NAME
```

Default models:
- OpenAI: `gpt-4o`
- Anthropic: `claude-3-opus-20240229`
- Ollama: `llama2`
- Compatible: `default`

### API Configuration

```bash
--api-key YOUR_API_KEY          # API key (or use environment variable)
--base-url https://api.example.com/v1  # For Ollama or compatible providers
--x-api-key HEADER_VALUE        # Custom API key header
```

### Output Options

```bash
--output FILENAME               # Output file (default: generated_app.py)
--no-validate                   # Skip code validation
```

## Examples

### Example 1: Simple Counter

```bash
p2m imagine "Create a counter app with:
- A display showing the current count
- An Increment button
- A Decrement button
- A Reset button"
```

### Example 2: Todo List

```bash
p2m imagine "Create a todo app with:
- A title 'My Tasks'
- An input field to add new todos
- A button to add todos
- A list of todos with delete buttons
- Show total and completed count"
```

### Example 3: Contact Form

```bash
p2m imagine "Create a contact form with:
- Title 'Contact Us'
- Name input field
- Email input field
- Message textarea
- Submit button
- Show success message after submit"
```

### Example 4: Dashboard

```bash
p2m imagine "Create a dashboard with:
- Header with title 'Dashboard'
- Three metric cards:
  - Users: 1,234
  - Orders: 567
  - Revenue: \$89,012
- A refresh button
- Use different colors for each card"
```

### Example 5: Product List

```bash
p2m imagine "Create a product listing app with:
- Product grid showing:
  - Product image
  - Product name
  - Price
  - Rating
  - Add to cart button
- Search bar at the top
- Filter by category"
```

## Environment Variables

### OpenAI

```bash
export OPENAI_API_KEY="sk-..."
```

### Anthropic

```bash
export ANTHROPIC_API_KEY="sk-ant-..."
```

### Ollama

```bash
export OLLAMA_BASE_URL="http://localhost:11434"
```

### Custom API

```bash
export P2M_COMPATIBLE_API_KEY="your-api-key"
```

## Workflow

### 1. Generate Code

```bash
p2m imagine "Create a simple app" --provider ollama --base-url https://ollama.dataseed.com.br --model qwen3-coder:latest
```

### 2. Review Generated Code

```bash
cat generated_app.py
```

### 3. Run the App

```bash
p2m run
```

### 4. Build for Production

```bash
p2m build --target android
p2m build --target ios
p2m build --target web
```

## Validation

The generated code is automatically validated to ensure:

- ✅ Valid Python syntax
- ✅ Imports from `p2m.core` and `p2m.ui`
- ✅ Defines `create_view()` function
- ✅ Returns `component.build()`

If validation fails, the error message will indicate what needs to be fixed.

## Tips for Better Results

### 1. Be Specific

**Good:**
```bash
p2m imagine "Create a todo app with:
- Input field to add new todos
- List showing all todos
- Delete button for each todo
- Show count of remaining todos"
```

**Less Good:**
```bash
p2m imagine "Create a todo app"
```

### 2. Describe Layout

```bash
p2m imagine "Create a form with:
- Title at the top
- Name input field
- Email input field below name
- Message textarea below email
- Submit button at the bottom"
```

### 3. Specify Styling

```bash
p2m imagine "Create a card with:
- White background
- Rounded corners
- Shadow effect
- Blue title text
- Gray body text"
```

### 4. Mention Interactions

```bash
p2m imagine "Create a button that:
- Shows 'Click Me' text
- Has blue background
- Changes to green when clicked
- Shows a message after clicking"
```

## Troubleshooting

### Error: "OPENAI_API_KEY not set"

**Solution:** Set the environment variable:

```bash
export OPENAI_API_KEY="sk-..."
p2m imagine "Create an app"
```

Or use the `--api-key` option:

```bash
p2m imagine "Create an app" --api-key "sk-..."
```

### Error: "Cannot connect to Ollama"

**Solution:** Make sure Ollama is running:

```bash
ollama serve
```

Or use a remote Ollama server:

```bash
p2m imagine "Create an app" \
  --provider ollama \
  --base-url https://ollama.dataseed.com.br \
  --model qwen3-coder:latest
```

### Error: "Code validation failed"

**Solution:** The LLM generated invalid code. Try:

1. Use a more specific description
2. Use a different model
3. Use the `--no-validate` flag to skip validation (not recommended)

### Error: "Syntax error in generated code"

**Solution:** The LLM generated code with syntax errors. Try:

1. Use a more detailed description
2. Specify the structure more clearly
3. Try a different provider or model

## Supported LLM Providers

### OpenAI

- **Models:** gpt-4o, gpt-4-turbo, gpt-3.5-turbo
- **Cost:** Paid API
- **Speed:** Fast
- **Quality:** Excellent

```bash
p2m imagine "Create an app" --provider openai --model gpt-4o
```

### Anthropic (Claude)

- **Models:** claude-3-opus, claude-3-sonnet, claude-3-haiku
- **Cost:** Paid API
- **Speed:** Medium
- **Quality:** Excellent

```bash
p2m imagine "Create an app" --provider anthropic --model claude-3-opus-20240229
```

### Ollama (Local)

- **Models:** llama2, mistral, neural-chat, qwen3-coder
- **Cost:** Free (local)
- **Speed:** Depends on hardware
- **Quality:** Good

```bash
p2m imagine "Create an app" --provider ollama --base-url http://localhost:11434 --model qwen3-coder:latest
```

### OpenAI-Compatible

- **Models:** Any OpenAI-compatible API
- **Cost:** Varies
- **Speed:** Varies
- **Quality:** Varies

```bash
p2m imagine "Create an app" \
  --provider openai-compatible \
  --base-url https://api.example.com/v1 \
  --api-key your-key \
  --model your-model
```

## Advanced Usage

### Batch Generation

```bash
# Generate multiple apps
for app in "counter" "todo" "form"; do
  p2m imagine "Create a $app app" --output "${app}_app.py"
done
```

### Custom Output Directory

```bash
p2m imagine "Create an app" --output ./generated/my_app.py
```

### Piping to Editor

```bash
p2m imagine "Create an app" --output - | less
```

### Integration with Scripts

```python
from p2m.imagine import imagine_command

success, message, code = imagine_command(
    description="Create a Hello World app",
    provider="openai",
    model="gpt-4o",
    api_key="sk-...",
)

if success:
    print(f"Generated code:\n{code}")
else:
    print(f"Error: {message}")
```

## Best Practices

1. **Start Simple** - Generate a basic app first, then iterate
2. **Be Descriptive** - More details lead to better results
3. **Validate Code** - Always review generated code before running
4. **Use Version Control** - Track changes to generated code
5. **Test Thoroughly** - Test the generated app before deployment

## Performance Notes

- **OpenAI:** Fastest, best quality, costs money
- **Anthropic:** Good quality, medium speed, costs money
- **Ollama:** Free, local, quality depends on model
- **Compatible APIs:** Varies by provider

## Next Steps

After generating code with `p2m imagine`:

1. Review the generated code
2. Run `p2m run` to test in development
3. Make any necessary adjustments
4. Build for production with `p2m build`
5. Deploy to your target platform

---

**Happy coding with P2M Imagine!** 🚀
