
import streamlit as st
import json
import os
if "review_data" not in st.session_state:
    st.session_state["review_data"] = None
from streamlit_copy_to_clipboard_button import copy_to_clipboard
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

st.set_page_config(
    page_title="SOLA | AI Content Review Studio",
    page_icon="🌞",
    layout="wide"
)


st.title("☀️ SOLA")
st.subheader("AI Content Review Studio")
st.write(
    "Smarter content reviews for confident marketing decisions. "
    "Evaluate brand voice, clarity, claims, and audience relevance."
)



st.divider()

left_col, right_col = st.columns([1, 1.2], gap="large")

with left_col:
    with st.container(border=True):
        st.subheader("01 | Brand Context")
        st.caption("Optional details to make your review more relevant.")

        brand_voice = st.text_input(
            "Brand voice",
            placeholder="Example: Friendly, confident, and conversational"
        )

        target_audience = st.text_input(
            "Target audience",
            placeholder="Example: Busy professionals ages 25-45"
        )

        verified_claims = st.text_area(
            "Verified product information",
            placeholder="Enter only facts or benefits you can support.",
            height=140
        )

with right_col:
    with st.container(border=True):
        st.subheader("02 | Content to Review")

        content_type = st.selectbox(
            "Content type",
            ["Instagram Caption", "Marketing Email"]
        )

        draft = st.text_area(
            "Your marketing draft",
            height=220,
            placeholder="Paste your marketing content here..."
        )

        st.caption(
            f"{len(draft)} characters  |  "
            f"{len(draft.split())} words"
        )

st.divider()


flagged_phrases = [
    "best ever",
    "guaranteed",
    "100% effective",
    "cures",
    "miracle"
]

found_phrases = [
    phrase for phrase in flagged_phrases
    if phrase in draft.lower()
]

if found_phrases:
    st.warning(
        "⚠️ Potential claims to review: "
        + ", ".join(found_phrases)
    )

if st.button("Review Content"):
    if not draft.strip():
        st.warning("Please enter some marketing content first.")
    else:
        
        with st.spinner("SOLA is reviewing your content..."):
             
                response = client.responses.create(
                    model="gpt-4.1-mini",
                    instructions="""
                    You are a marketing content reviewer for SOLA,
an AI-assisted content review application.

Review marketing content for different brands and industries.
Do not assume a specific brand personality, target audience,
or product unless that information is provided.

When brand guidelines are unavailable, evaluate Brand Voice
based on consistency, professionalism, and suitability
for the content type. State when brand-specific information
is needed for a more accurate assessment.

                    Review the content using these five categories:
                    1. Brand Voice
                    2. Message Clarity
                    3. Claims & Accuracy
                    4. Call to Action
                    5. Audience Relevance
    Review conservatively. Do not invent problems to justify a revision.
Do not invent product benefits, performance results,
statistics, guarantees, or customer experiences.

When rewriting unsupported claims, remove the claims
rather than replacing them with new unverified claims.

Only describe product benefits when those benefits
are explicitly supported by information provided
in the draft or brand context.

If sufficient information is unavailable, create
a neutral revision that focuses on the product
without promising specific results.
When no verified product benefits are provided, use only
neutral product descriptions and calls to action.

For example, a skincare product may be described as
"a skincare cream," but do not claim it nourishes,
hydrates, refreshes, smooths, repairs, or improves skin
without supporting information.

Before returning a suggested revision, check every
statement for newly introduced product claims.

When revising marketing copy, distinguish between
creative promotional language and factual product claims.

Do not introduce unverified statements about product
effectiveness, suitability for particular routines,
performance, convenience, or customer results.

For skincare products, phrases such as "effective skincare,"
"perfect for your daily routine," or "improves your skin"
require supporting product information.

You may improve subject lines, sentence structure,
emotional appeal, and calls to action without
inventing new product benefits.

Before finalizing a revision, compare every product-related
statement against the verified product information.
If a statement cannot be supported, remove or rewrite it
using neutral, factual language.

Remove any claim not supported by the supplied content
or verified product information.
    A clear, relevant call to action such as "Explore the collection today" should receive Pass.

    Only mark Needs Improvement when there is a meaningful issue that affects clarity, brand consistency, or effectiveness.

    Treat optional creative alternatives as suggestions, not defects.

    If the original content is already appropriate, say so. Do not rewrite it unnecessarily.
                    For each category, choose:
                    Pass, Needs Improvement, or Flagged.

                    Explain any issues and suggest a revised version.
                    Preserve the original message and meaning.
                    Do not automatically approve publication.
    Claims & Accuracy rules:

    Mark unsupported health or wellness claims as Flagged, especially guarantees about eliminating stress, curing conditions, or producing specific health benefits.

    When suggesting revisions, remove unsupported claims completely. Do not simply replace a strong claim with a softer version of the same claim.

    
    Before returning a suggested revision, check it for new unsupported claims. If any remain, revise it again.

    All findings are advisory and require human review.
                    Return your review as valid JSON only.

    Use this exact structure:
    {
    "reviews": [
        {
        "category": "Brand Voice",
        "status": "Pass",
        "explanation": "Your explanation here"
        }
    ],
    "suggested_revision": null
    }

    Include all five review categories.
    For each category, status must be exactly:
    "Pass", "Needs Improvement", or "Flagged".

    Use null for suggested_revision when no changes are needed.
    Otherwise provide one complete revised draft.
    Do not include Markdown code fences.
    """,
    input=(
    f"Content type: {content_type}\n\n"
    f"Brand voice: {brand_voice or 'Not provided'}\n"
    f"Target audience: {target_audience or 'Not provided'}\n"
    f"Verified product information: {verified_claims or 'Not provided'}\n\n"
    f"Draft:\n{draft}"
)
                )
        
        # Save the completed review for future reruns.
        
        # Save the completed review for future reruns.
        try:
            review_data = json.loads(response.output_text)

            if not isinstance(review_data.get("reviews"), list):
                raise ValueError("Missing reviews")

            revision = review_data.get("suggested_revision")
            safety_warning = None

            if revision:
                try:
                    safety_response = client.responses.create(
                        model="gpt-4.1-mini",
                        instructions="""
You are an independent marketing claim checker.

Examine the AI-suggested revision against the
verified product information.

Identify newly introduced factual product claims
that are not supported by verified information.

Check performance, effectiveness, suitability,
safety, gentleness, convenience, guarantees,
and implied product benefits.

Ordinary creative wording and calls to action
are not automatically unsupported claims.

Do not treat the suggested revision as evidence
that its own claims are true.

Respond using valid JSON only:
{
  "unsupported_claims": [
    "Exact unsupported phrase"
  ]
}

If there are no unsupported claims, return an
empty list. Do not use Markdown code fences.
""",
                        input=(
                            f"Verified product information:\n"
                            f"{verified_claims or 'Not provided'}\n\n"
                            f"Original draft:\n{draft}\n\n"
                            f"Suggested revision:\n{revision}"
                        )
                    )

                    safety_data = json.loads(
                        safety_response.output_text
                    )
                    unsupported = safety_data["unsupported_claims"]

                    if not isinstance(unsupported, list):
                        raise ValueError("Invalid safety results")

                    if unsupported:
                        safety_warning = (
                            "Potential unsupported claims in the "
                            "suggested revision:\n\n- "
                            + "\n- ".join(str(x) for x in unsupported)
                        )

                except Exception:
                    safety_warning = (
                        "The revision safety check could not be "
                        "completed. Please verify product claims manually."
                    )

            st.session_state["review_data"] = review_data
            st.session_state["reviewed_draft"] = draft
            st.session_state["revision_output"] = revision or ""
            st.session_state["safety_warning"] = safety_warning

        except (json.JSONDecodeError, ValueError, TypeError):
            st.error("The AI response could not be organized.")
            st.write(response.output_text)



# Display saved results independently of the Review Content button.
review_data = st.session_state["review_data"]

if review_data is not None:

    st.subheader("Original Content")
    st.info(st.session_state["reviewed_draft"])

    st.subheader("AI Review Results")

    columns = st.columns(2, gap="large")

    for index, item in enumerate(review_data["reviews"]):
        with columns[index % 2]:
            with st.container(border=True):

                st.markdown(f"### {item['category']}")

                if item["status"] == "Pass":
                    st.success("✅ Pass")
                elif item["status"] == "Flagged":
                    st.error("🚩 Flagged")
                else:
                    st.warning("⚠️ Needs Improvement")

                st.write(item["explanation"])

    revision = review_data.get("suggested_revision")

    if revision:
        st.subheader("✨ AI Suggested Revision")

        with st.container(border=True):
            st.text_area(
                "Revised marketing copy",
                height=120,
                key="revision_output"
            )
            copy_to_clipboard(
                st.session_state["revision_output"],
                label="📋 Copy Revision",
                label_after_copy="✅ Copied!"
)
            st.caption(
                "AI-generated suggestion. Review for accuracy, "
                "brand alignment, and unsupported claims before publishing."
            )
            
            if st.session_state.get("safety_warning"):
                st.warning(
                    st.session_state["safety_warning"]
                )


    else:
        if all(
        item.get("status") == "Pass"
        for item in review_data["reviews"]
    ):
            st.success("All review categories passed. No revision needed.")
        else:
            st.info(
            "No revised draft was suggested. Review the findings "
            "above for any areas that may need attention."
        )




