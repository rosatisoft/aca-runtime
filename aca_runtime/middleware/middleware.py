from __future__ import annotations

from typing import Any, Dict, Optional

from aca_runtime.runtime.atlas_measurements import measure_text_with_atlas
from aca_runtime.runtime.runtime_v2 import ACARuntimeV2
from aca_runtime.runtime.supervised_generation import ACASupervisedGenerator

from .request import MiddlewareMode, MiddlewareRequest
from .response import MiddlewareResponse


class ACAMiddleware:
    """
    Model-agnostic ACA Runtime middleware.

    This layer wraps Runtime v2 so applications can plug ACA into APIs,
    Streamlit apps, agent workflows, n8n flows, or LLM providers without
    duplicating precondition, trajectory, and post-generation supervision logic.

    The middleware supports three modes:
    - measure_only: Atlas measurement only; does not mutate runtime state.
    - supervise_only: Runtime v2 admission/state/application response; no LLM call.
    - generate: Runtime v2 + optional LLM provider + post-generation review.
    """

    def __init__(
        self,
        artifacts_root: Optional[str] = None,
        mode: MiddlewareMode = "supervise_only",
        runtime: Optional[ACARuntimeV2] = None,
        llm_provider: Optional[Any] = None,
        embedding_model: str = "text-embedding-3-small",
    ):
        self.artifacts_root = artifacts_root
        self.mode = mode
        self.embedding_model = embedding_model
        self.runtime = runtime or ACARuntimeV2(
            artifacts_root=artifacts_root,
            embedding_model=embedding_model,
        )
        self.llm_provider = llm_provider

    def handle(
        self,
        text: str,
        objective: Optional[str] = None,
        mode: Optional[MiddlewareMode] = None,
        metadata: Optional[Dict[str, Any]] = None,
    ) -> MiddlewareResponse:
        request = MiddlewareRequest(
            text=text,
            objective=objective,
            mode=mode or self.mode,
            metadata=metadata or {},
        )

        if request.mode == "measure_only":
            return self._measure_only(request)

        if request.mode == "supervise_only":
            return self._supervise_only(request)

        if request.mode == "generate":
            return self._generate(request)

        raise ValueError(f"Unsupported middleware mode: {request.mode}")

    def _measure_only(
        self,
        request: MiddlewareRequest,
    ) -> MiddlewareResponse:
        if self.artifacts_root is None:
            measurements_obj = measure_text_with_atlas(
                text=request.text,
                embedding_model=self.embedding_model,
            )
        else:
            measurements_obj = measure_text_with_atlas(
                text=request.text,
                artifacts_root=self.artifacts_root,
                embedding_model=self.embedding_model,
            )

        measurements = measurements_obj.to_dict()

        return MiddlewareResponse(
            mode=request.mode,
            input_text=request.text,
            objective=request.objective,
            admitted=False,
            action="MEASURE_ONLY",
            final_response=None,
            llm_called=False,
            should_call_llm=False,
            boundary_applied=False,
            measurements=measurements,
            metadata={
                "request": request.to_dict(),
                "state_mutated": False,
                "note": "Measurement mode does not mutate runtime state.",
            },
        )

    def _supervise_only(
        self,
        request: MiddlewareRequest,
    ) -> MiddlewareResponse:
        runtime_result = self.runtime.step(
            text=request.text,
            objective=request.objective,
        ).to_dict()

        application_response = runtime_result.get("application_response", {})

        return MiddlewareResponse(
            mode=request.mode,
            input_text=request.text,
            objective=request.objective,
            admitted=bool(runtime_result.get("admitted", False)),
            action=runtime_result.get("action", "UNKNOWN"),
            final_response=application_response.get("message"),
            llm_called=False,
            should_call_llm=bool(application_response.get("should_call_llm", False)),
            boundary_applied=bool(application_response.get("boundary_applied", False)),
            runtime_result=runtime_result,
            application_response=application_response,
            metadata={
                "request": request.to_dict(),
                "state_snapshot": runtime_result.get("state_snapshot"),
            },
        )

    def _generate(
        self,
        request: MiddlewareRequest,
    ) -> MiddlewareResponse:
        if self.llm_provider is None:
            supervised = self._supervise_only(request)
            supervised.metadata["generation_status"] = "provider_not_configured"
            supervised.metadata["generation_note"] = (
                "Generation mode requested, but no LLM provider was configured. "
                "Returning supervised runtime response without generation."
            )
            return supervised

        generator = ACASupervisedGenerator(
            runtime=self.runtime,
            llm_provider=self.llm_provider,
        )

        generation_result = generator.step(
            text=request.text,
            objective=request.objective,
        ).to_dict()

        runtime_result = generation_result.get("runtime_result", {})
        application_response = runtime_result.get("application_response", {})

        return MiddlewareResponse(
            mode=request.mode,
            input_text=request.text,
            objective=request.objective,
            admitted=bool(runtime_result.get("admitted", False)),
            action=runtime_result.get("action", "UNKNOWN"),
            final_response=generation_result.get("final_response"),
            llm_called=bool(generation_result.get("llm_called", False)),
            should_call_llm=bool(application_response.get("should_call_llm", False)),
            boundary_applied=bool(application_response.get("boundary_applied", False)),
            runtime_result=runtime_result,
            application_response=application_response,
            llm_response=generation_result.get("llm_response"),
            post_generation_review=generation_result.get("post_generation_review"),
            metadata={
                "request": request.to_dict(),
                "state_snapshot": runtime_result.get("state_snapshot"),
            },
        )

    def snapshot(self) -> Dict[str, Any]:
        return self.runtime.snapshot()
