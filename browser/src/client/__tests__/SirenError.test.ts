import { describe, expect, it } from "vitest";
import { SirenResponseError, sirenResponseError } from "../SirenError";

function response(
  body: BodyInit | null,
  status: number,
  contentType = "application/vnd.siren+json",
): Response {
  return new Response(body, {
    headers: { "Content-Type": contentType },
    status,
    statusText: status === 404 ? "Not Found" : "Unprocessable Content",
  });
}

describe("sirenResponseError", () => {
  it("projects structured violations onto matching action fields", async () => {
    const error = await sirenResponseError(
      response(
        JSON.stringify({
          class: ["error"],
          properties: {
            detail: [
              {
                location: "language_id",
                message: "Select a supported language.",
              },
              {
                loc: ["body", "body", "spec", "templates", 0, "path"],
                msg: "This path is required.",
              },
            ],
          },
          title: "Validation failed",
        }),
        422,
      ),
      ["language_id", "spec"],
    );

    expect(error).toBeInstanceOf(SirenResponseError);
    expect(error).toMatchObject({
      fieldErrors: {
        language_id: "Select a supported language.",
        spec: "This path is required.",
      },
      status: 422,
      title: "Validation failed",
    });
    expect(error.details).toEqual([
      "language_id: Select a supported language.",
      "spec.templates[0].path: This path is required.",
    ]);
    expect(error.message).toBe(
      "Validation failed: language_id: Select a supported language. spec.templates[0].path: This path is required.",
    );
    expect(error.entity?.class).toEqual(["error"]);
  });

  it("projects a missing resource detail into the error message", async () => {
    const error = await sirenResponseError(
      response(
        JSON.stringify({
          class: ["error"],
          properties: { detail: "Resource not found." },
          title: "Scaffolding",
        }),
        404,
      ),
    );

    expect(error.message).toBe("Scaffolding: Resource not found.");
    expect(error.details).toEqual(["Resource not found."]);
  });

  it.each([
    ["an HTML response", "<h1>Gateway error</h1>", "text/html"],
    ["an empty response", "", "application/json"],
    ["malformed JSON", "{not-json", "application/vnd.siren+json"],
  ])(
    "uses the HTTP status fallback for %s",
    async (_name, body, contentType) => {
      const error = await sirenResponseError(response(body, 422, contentType));

      expect(error).toMatchObject({
        details: [],
        fieldErrors: {},
        message: "Unprocessable Content",
        status: 422,
      });
      expect(error.entity).toBeUndefined();
    },
  );
});
