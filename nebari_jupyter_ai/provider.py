from functools import wraps
from typing import ClassVar, List, Type

from jupyter_ai import AuthStrategy, BaseProvider, Field
from jupyter_ai_magics.partner_providers.openai import ChatOpenAIProvider
from jupyter_ai_magics.models.persona import Persona

from .llm import TestLLM

NEBARI_CHAT_SYSTEM_PROMPT = """
You are Nebari Assistant, a conversational assistant living in Nebari to help users.

Nebari is an open-source data science platform that deploys on Kubernetes and helps data science teams manage their infrastructure, environments, and collaboration.

**Core Information about Nebari:**

Nebari automates the provisioning of cloud infrastructure, deploys a Kubernetes cluster, and configures various services to provide a complete platform. It allows users to focus on data science and model building rather than systems administration.

**Key Components and Concepts:**

*   **Kubernetes:** Nebari deploys on Kubernetes, Users are not expected to know or understand Kubernetes, but Kubernetes concepts like pods, deployments, services, and namespaces is helpful for debugging.
*   **Terraform:** Nebari uses OpenTofu to provision and manage cloud resources.
*   **Helm:** Nebari uses Helm to manage application deployments within the Kubernetes cluster.
*   **Conda-store:** Nebari uses conda-store to manage user environments. Users can create, share, and reproduce environments using conda-store. Environments must include `ipykernel` and `ipywidgets` to function correctly in JupyterLab. Environments are associated with namespaces. By default, there are `nebari-git` and `global` namespaces, in addition to user specific namespaces, such as user's user name, for example `test-user`. The `nebari-git` namespace is for environments created with the `nebari-config.yaml`. The `global` namespace is used by conda-store internally. If the environment isn't showing up, make sure ipykernel and ipywidgets are included in the env config.
*   **JupyterHub:** Provides a multi-user Jupyter Notebook environment. Users authenticate via Keycloak and are then able to launch JupyterLab or other services.  Users interface with you via a Jupyterlab extension.
*   **Jhub Apps:** A jupyterhub managed service that allows users to launch dashboards and other custom applications from JupyterHub and optionally share them with others.
*   **Keycloak:** Provides authentication and authorization for the Nebari platform. It manages users, groups, and roles. By default, the groups 'admin', 'developer', and 'analyst' are created. It is accessible at `<nebari-url>/auth/admin/`. Initial root password for Keycloak is generated during Nebari initialization and stored in the `nebari-config.yaml` during initialization.
*   **Dask Gateway:** Enables users to create and manage Dask clusters for distributed computing. Dask workers are deployed in Kubernetes pods.
*   **Traefik:** An Ingress controller that manages routing traffic to services within the Kubernetes cluster. It also handles SSL certificate management (e.g., using Let's Encrypt).
*   **CI/CD:** Continuous Integration/Continuous Deployment pipelines. Nebari can generate pipelines for GitHub Actions and GitLab CI. The CI/CD pipeline is responsible for automatically redeploying Nebari when changes are made to the configuration.
*   **Shared File System:** Provides a persistent volume for storing user data and shared resources. Uses NFS by default, but can use Ceph.

You are not a language model, but rather an application built on a foundation model from {provider_name} called {local_model_id}.
You are talkative and you provide lots of specific details from the foundation model's context.
You may use Markdown to format your response.
If your response includes code, they must be enclosed in Markdown fenced code blocks (with triple backticks before and after).
If your response includes mathematical notation, they must be expressed in LaTeX markup and enclosed in LaTeX delimiters.
All dollar quantities (of USD) must be formatted in LaTeX, with the `$` symbol escaped by a single backslash `\\`.
- Example prompt: `If I have \\\\$100 and spend \\\\$20, how much money do I have left?`
- **Correct** response: `You have \\(\\$80\\) remaining.`
- **Incorrect** response: `You have $80 remaining.`
If you do not know the answer to a question, answer truthfully by responding that you do not know.
The following is a friendly conversation between you and a human.
""".strip()


def with_nebari_prompt(original_method):
    @wraps(original_method)
    def wrapper(self, *args, **kwargs):
        from jupyter_ai_magics import providers

        # Store original prompt
        original_prompt = providers.CHAT_SYSTEM_PROMPT
        
        # Replace with custom prompt temporarily
        # global CHAT_SYSTEM_PROMPT
        providers.CHAT_SYSTEM_PROMPT = NEBARI_CHAT_SYSTEM_PROMPT
        
        try:
            # Call original method with our custom prompt
            return original_method(self, *args, **kwargs)
        finally:
            # Restore original prompt
            CHAT_SYSTEM_PROMPT = original_prompt
            
    return wrapper


# def apply_nebari_prompt(cls: Type) -> Type:
#     """Class decorator that applies the Nebari prompt wrapper to all methods"""
#     for attr_name, attr_value in vars(cls).items():
#         if callable(attr_value) and not attr_name.startswith('__'):
#             setattr(cls, attr_name, with_nebari_prompt(attr_value))
#     return cls

# JUPYTERNAUT_AVATAR_ROUTE = "api/ai/static/jupyternaut.svg"
NEBARI_ASSISTANT_AVATAR_ROUTE = "nebari-jupyter-ai/static/nebari-logo-with-bg.svg"

# @apply_nebari_prompt
class TestProvider(ChatOpenAIProvider):
    id = "nebari-provider"
    name = "Nebari Provider"
    
    persona = Persona(name="Nebari Assistant", avatar_route=NEBARI_ASSISTANT_AVATAR_ROUTE)

    @with_nebari_prompt
    def get_chat_prompt_template(self):
        return super().get_chat_prompt_template()



# class TestProvider(BaseProvider, TestLLM):
#     """
#     A test model provider implementation for developers to build from. A model
#     provider inherits from 2 classes: 1) the `BaseProvider` class from
#     `jupyter_ai`, and 2) an LLM class from `langchain`, i.e. a class inheriting
#     from `LLM` or `BaseChatModel`.

#     Any custom model first requires a `langchain` LLM class implementation.
#     Please import one from `langchain`, or refer to the `langchain` docs for
#     instructions on how to write your own. We offer an example in `./llm.py` for
#     testing.

#     To create a custom model provider from an existing `langchain`
#     implementation, developers should edit this class' declaration to

#     ```
#     class TestModelProvider(BaseProvider, <langchain-llm-class>):
#         ...
#     ```

#     Developers should fill in each of the below required class attributes.
#     As the implementation is provided by the inherited LLM class, developers
#     generally don't need to implement any methods. See the built-in
#     implementations in `jupyter_ai_magics.providers.py` for further reference.

#     The provider is made available to Jupyter AI by the entry point declared in
#     `pyproject.toml`. If this class or parent module is renamed, make sure the
#     update the entry point there as well.
#     """

#     id: ClassVar[str] = "test-provider"
#     """ID for this provider class."""

#     name: ClassVar[str] = "Test Provider"
#     """User-facing name of this provider."""

#     models: ClassVar[List[str]] = ["test-model-1"]
#     """List of supported models by their IDs. For registry providers, this will
#     be just ["*"]."""

#     help: ClassVar[str] = None
#     """Text to display in lieu of a model list for a registry provider that does
#     not provide a list of models."""

#     model_id_key: ClassVar[str] = "model_id"
#     """Kwarg expected by the upstream LangChain provider."""

#     model_id_label: ClassVar[str] = "Model ID"
#     """Human-readable label of the model ID."""

#     pypi_package_deps: ClassVar[List[str]] = []
#     """List of PyPi package dependencies."""

#     auth_strategy: ClassVar[AuthStrategy] = None
#     """Authentication/authorization strategy. Declares what credentials are
#     required to use this model provider. Generally should not be `None`."""

#     registry: ClassVar[bool] = False
#     """Whether this provider is a registry provider."""

#     fields: ClassVar[List[Field]] = []
#     """User inputs expected by this provider when initializing it. Each `Field` `f`
#     should be passed in the constructor as a keyword argument, keyed by `f.key`."""
