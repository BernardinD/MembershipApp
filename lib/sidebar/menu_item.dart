import 'package:flutter/material.dart';

class MenuItem extends StatelessWidget {
  final IconData icon;
  final String title;
  final Function onTap;
  final double width;

  const MenuItem({Key key, this.icon, this.title, this.onTap, this.width}) : super(key: key);

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTap: onTap,
      child: Container(
        // The Gesture doesn't apply to whole row with the Decoration for some reason
        decoration: BoxDecoration(
        ),
          child: Padding(
            padding: const EdgeInsets.all(16),
              child: Row(
                children: <Widget>[
                  Icon(
                    icon,
                    color: Colors.cyan,
                    size: 30,
                  ),
                  SizedBox(
                    width: 20,
                  ),
                  Text(
                    title,
                    style: TextStyle(fontWeight: FontWeight.w300, fontSize: 26, color: Colors.white),
                  )
                ],
              ),
            ),
      ),
    );
  }
}
