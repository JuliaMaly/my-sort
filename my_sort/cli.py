import sys
import click

@click.command(context_settings=dict(help_option_names=["-h", "--help"]))
@click.option("-r", "--reverse", is_flag=True, help="Reverse the sort order.")
@click.option("-n", "--numeric", is_flag=True, help="Compare according to string numerical value.")
@click.argument("files", nargs=-1, type=click.File("r"), required=False)
def main(reverse, numeric, files):
    """
    my-sort: simple implementation of unix sort with -r and -n.

    If no FILE is given, read from stdin.
    """
    if not files:
        lines = sys.stdin.read().splitlines()
    else:
        lines = []
        for f in files:
            lines.extend(f.read().splitlines())

    def key_func(s):
        if numeric:
            try:
                return float(s)
            except Exception:
                # if cannot parse, fallback to original string but ensure consistent ordering
                return float("inf"), s
        else:
            return s

    # For numeric: stable sort with key. For strings: normal sort.
    if numeric:
        # We want lines that can be numeric to come before non-numeric; above key returns inf for non-num.
        try:
            sorted_lines = sorted(lines, key=lambda s: (float(s) if _is_float(s) else float("inf"), s), reverse=reverse)
        except Exception:
            # Fallback safe method: attempt convert with try
            def numeric_key(s):
                try:
                    return (0, float(s))
                except:
                    return (1, s)
            sorted_lines = sorted(lines, key=numeric_key, reverse=reverse)
    else:
        sorted_lines = sorted(lines, reverse=reverse)

    for ln in sorted_lines:
        click.echo(ln)

def _is_float(s):
    try:
        float(s)
        return True
    except:
        return False

if __name__ == "__main__":
    main()