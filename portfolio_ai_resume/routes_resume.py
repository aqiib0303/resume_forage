from flask import Blueprint, render_template, request, abort, make_response
import pdfkit
import os

bp = Blueprint("resume", __name__)

# Central wkhtmltopdf config
WKHTMLTOPDF_PATH = r"C:\Program Files\wkhtmltopdf\bin\wkhtmltopdf.exe"
PDF_CONFIG = pdfkit.configuration(wkhtmltopdf=WKHTMLTOPDF_PATH)

# Templates meta (free/premium toggle)
TEMPLATES = {
    "modern": {"name": "Modern Resume", "premium": False},
    "minimal": {"name": "Minimal Resume", "premium": False},
    "creative": {"name": "Creative Resume", "premium": True},
    "ats_friendly": {"name": "ATS Friendly Resume", "premium": False},
    "ats_modern": {"name": "ATS Modern Resume", "premium": False},
    "premium_modern_pro": {"name": "Premium Modern Pro Resume", "premium": False},
}


def build_payload(form):
    """Convert raw form into structured payload."""
    name = form.get("name", "").strip()
    role = form.get("role", "").strip()
    summary = form.get("summary", "").strip()
    skills = [s.strip() for s in form.getlist("skills[]") if s.strip()]

    # Work Experience
    exp_companies = form.getlist("exp_company[]")
    exp_roles = form.getlist("exp_role[]")
    exp_dates = form.getlist("exp_dates[]")
    exp_descs = form.getlist("exp_desc[]")
    experiences = []
    for i in range(max(len(exp_companies), len(exp_roles), len(exp_dates), len(exp_descs))):
        c = exp_companies[i] if i < len(exp_companies) else ""
        r = exp_roles[i] if i < len(exp_roles) else ""
        d = exp_dates[i] if i < len(exp_dates) else ""
        desc = exp_descs[i] if i < len(exp_descs) else ""
        if c.strip() or r.strip() or d.strip() or desc.strip():
            experiences.append(
                {"company": c.strip(), "role": r.strip(), "dates": d.strip(), "desc": desc.strip()}
            )

    # Education
    edu_schools = form.getlist("edu_school[]")
    edu_degrees = form.getlist("edu_degree[]")
    edu_dates = form.getlist("edu_dates[]")
    education = []
    for i in range(max(len(edu_schools), len(edu_degrees), len(edu_dates))):
        s = edu_schools[i] if i < len(edu_schools) else ""
        deg = edu_degrees[i] if i < len(edu_degrees) else ""
        d = edu_dates[i] if i < len(edu_dates) else ""
        if s.strip() or deg.strip() or d.strip():
            education.append({"school": s.strip(), "degree": deg.strip(), "dates": d.strip()})

    if not name:
        abort(400, "Name is required")

    return {
        "name": name,
        "role": role,
        "summary": summary,
        "skills": skills,
        "experiences": experiences,
        "education": education,
    }


@bp.get("/builder")
def builder():
    return render_template("resume/builder.html")


@bp.post("/render/<template_name>")
def render_resume(template_name):
    """Render chosen resume template."""
    data = build_payload(request.form)

    # security: only allow from list
    allowed_templates = [
        "modern.html",
        "classic.html",
        "minimal.html",
        "ats_modern",
        "premium_modern_pro.html",
        "ats_friendly",
    ]

    if f"{template_name}.html" not in allowed_templates:
        return "Template not found", 404

    return render_template(f"resume_templates/{template_name}.html", data=data)




@bp.post("/preview/<style>")
def preview(style):
    """Preview resume in chosen style."""
    if style not in TEMPLATES:
        abort(404, "Template not found")
    data = build_payload(request.form)
    return render_template(f"resume_templates/{style}.html", data=data)


@bp.post("/download/<style>")
def download(style):
    """Download resume as PDF using pdfkit."""
    if style not in TEMPLATES:
        abort(404, "Template not found")

    data = build_payload(request.form)
    html = render_template(f"resume_templates/{style}.html", data=data)

    # Generate PDF
    pdf = pdfkit.from_string(html, False, configuration=PDF_CONFIG)

    filename = f"{data['name'].replace(' ', '_')}_{style}_resume.pdf"

    response = make_response(pdf)
    response.headers["Content-Type"] = "application/pdf"
    response.headers["Content-Disposition"] = f"attachment; filename={filename}"
    return response


@bp.route("/preview_templates")
def preview_templates():
    """Show all available templates (free + premium)."""
    return render_template("resume/preview_templates.html", templates=TEMPLATES)

# 📌 Blog Route
@bp.route("/blog")
def blog():
    """Show blog page with articles and template-related content."""
    return render_template("resume/blog.html")


# 📌 Contact Route
@bp.route("/contact")
def contact():
    """Show contact page with WhatsApp link and developer info."""
    return render_template("resume/contact.html")
