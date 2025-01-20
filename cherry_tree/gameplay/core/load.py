def load_context_from_config(config, context):
    context["combat"] = config["combat"].copy()
    context["slayerHunting"] = config["slayerHunting"].copy()
    context["gameWindow"]["name"] = config["gameWindow"]["name"]

    return context
