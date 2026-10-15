
"""Command registration using the Decorator Pattern."""


class CommandRegistry:
    """Register commands and generate help dynamically."""

    def __init__(self):
        self._commands = {}
        self._descriptions = {}

    def register(self, name, description):
        """Decorator to register a command."""

        def decorator(command_class):
            self._commands[name] = command_class
            self._descriptions[name] = description
            return command_class

        return decorator

    def get_command(self, name):
        """Retrieve a registered command class."""
        return self._commands.get(name)

    def get_help(self):
        """Generate help text from registered commands."""
        lines = ["Available commands:"]

        for name, description in self._descriptions.items():
            lines.append(f"  {name} - {description}")

        return "\n".join(lines)

    def list_commands(self):
        """Return all registered command names."""
        return list(self._commands.keys())
